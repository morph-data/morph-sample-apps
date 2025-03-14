from typing import Generator

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from morph_lib.database import execute_sql
from morph_lib.stream import stream_chat
from morph_lib.types import MorphChatStreamChunk

import morph
from morph import MorphGlobalContext

SYSTEM_TEMPLATE = """Please execute SQL queries on a table named `./data/Traffic_Orders_Demo_Data.csv` in DuckDB with the following schema:
date: text - date
source: text - traffic source (Coupon, Google Organic など)
traffic: int - traffic count
orders: int - order count

This table contains traffic and order data for the marketing campaigns.

As a source, you have the following data:
- Coupon
- Google Organic
- Google Paid
- TikTok Ads
- Meta Ads
- Referral

Generate a SQL query to answer the user's question.
{format_instructions}
"""

@morph.func
def sql_agent(
    context: MorphGlobalContext,
) -> Generator[MorphChatStreamChunk, None, None]:
    chat = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        streaming=False,
    )

    # Setup the SQL query output parser
    sql_schema = ResponseSchema(name="sql", description="The SQL query to execute")
    output_parser = StructuredOutputParser.from_response_schemas([sql_schema])
    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_TEMPLATE),
        ("human", "{question}")
    ])

    # Create the chain for SQL generation
    chain = (
        {"question": RunnablePassthrough(), "format_instructions": lambda _: format_instructions}
        | prompt
        | chat
        | StrOutputParser()
        | output_parser
    )

    # Generate SQL query
    result = chain.invoke(context.vars["prompt"])
    sql = result["sql"]
    # display generated sql
    yield stream_chat(f"""
### SQL
```sql
{sql}
```
""")

    # Execute SQL and get results
    data = execute_sql(sql, "DUCKDB")
    data_md = data.to_markdown(index=False)
    # Create analysis prompt with results
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""Please answer in markdown format.
You can use the following data:
{data_md}

The data is from the following SQL query:
{sql}
"""),
        ("human", "{question}")
    ])

    # Create analysis chain
    analysis_chain = (
        {"question": RunnablePassthrough()}
        | analysis_prompt
        | chat
    )

    # stream analysis result
    for chunk in analysis_chain.stream(context.vars["prompt"]):
        if chunk.content:
            yield stream_chat(chunk.content)
