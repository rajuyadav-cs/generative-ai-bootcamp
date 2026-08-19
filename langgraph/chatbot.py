# importing all the neccessary things
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import add_messages, START, END, StateGraph
from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


class State(TypedDict):
    
    messages : Annotated[list[BaseMessage], add_messages]

llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.4,
    max_tokens = 2000 
    
)


def chat_mode(state: State) -> State:
    messages = state["messages"]

    response = llm.invoke(messages)
    content = response.content

    if "<think>" in content:
        content = content.split("</think>")[-1].strip()

    return {
        "messages": [AIMessage(content=content)]
    }

checkpointer = MemorySaver()
graph = StateGraph(State)
graph.add_node("chat_mode", chat_mode)
graph.add_edge(START, "chat_mode")
graph.add_edge("chat_mode", END)

app = graph.compile(checkpointer= checkpointer)

# os.makedirs("images", exist_ok= True)
# with open("images/graph.png", "wb") as f:
#     pngimg = app.get_graph().draw_mermaid_png()
#     f.write(pngimg)

thread_id = "1"
while True:
    
    user_message = input("\nYOU: ")
    if user_message.strip().lower() in ["exit", "shutdown", "close", "switchoff", "quit"]:
        break 
    
    config = {
        "configurable": {"thread_id": thread_id}
    }
    result = app.invoke({
        "messages":[ HumanMessage(content=user_message)],
    }, config= config)
    
    
    print(f"\nAI: {result['messages'][-1].content}")
    # print(result)