from typing import TypedDict, Annotated
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")

if not DB_URI:
    raise ValueError("DATABASE_URL is not set in .env")

# PostgreSQL checkpointer
checkpointer_cm = PostgresSaver.from_conn_string(DB_URI)
checkpointer = checkpointer_cm.__enter__()

# Create required tables
checkpointer.setup()

# LLM
llm = init_chat_model(
    model=os.getenv("MODEL"),
    model_provider=os.getenv("PROVIDER"),
    temperature=0.4,
)


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chatmodel(state: State):
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


# Graph
graph = StateGraph(State)

graph.add_node("chat", chatmodel)

graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# Compile
app = graph.compile(
    checkpointer=checkpointer
)