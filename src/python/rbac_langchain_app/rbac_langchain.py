import os
import morph
from morph import MorphGlobalContext
from morph_lib.stream import create_chunk
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from morph_lib.stream import stream_chat

history = []

@morph.func
def rbac_langchain(context: MorphGlobalContext):
    # context.user_info comes from user's authentication info.
    if "admin" not in context.user_info["roles"]:
        yield stream_chat("You are not authorized to use this feature. \n\n Please login as admin.")
        return

    if len(history) > 3:
        history.pop(0)

    model = ChatOpenAI(model="gpt-4o-mini")
    prompt = context.vars["prompt"]
    thread_id = context.vars["thread_id"]

    thread = [x for x in history if x["thread_id"] == thread_id]

    if len(thread) == 0:
        messages = [
            SystemMessage(content="Please translate the following text from English to French."),
        ]
    else:
        messages = thread[0]["messages"]

    # chat
    messages.append(HumanMessage(content=prompt))

    result = ""
    for token in model.stream(messages):
        text = token.content
        result += text
        yield create_chunk(text)

    messages.append(AIMessage(content=result))

    history.append({
        "thread_id": thread_id,
        "messages": messages
    })