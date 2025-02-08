import morph
from morph import MorphGlobalContext
from morph_lib.stream import create_chunk
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from morph_lib.stream import stream_chat

history = {}

@morph.func
def rbac_langchain(context: MorphGlobalContext):
    # context.user_info comes from user's authentication info.
    if "admin" not in context.user_info["roles"]:
        yield stream_chat("You are not authorized to use this feature.")
        return

    model = ChatOpenAI(model="gpt-4o-mini")
    if history.get("thread_id") != context.vars["thread_id"]:
        history["thread_id"] = context.vars["thread_id"]
        history["messages"] = [
            SystemMessage(content="Please translate the following text from English to French."),
        ]
    history["messages"].append(HumanMessage(content=context.vars["prompt"]))

    result = ""
    for token in model.stream(history["messages"]):
        result += token.content
        yield create_chunk(token.content)
    history["messages"].append(AIMessage(content=result))