from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from typing import TypedDict
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
prompt = PromptTemplate.from_template("Answer the topic: {topic}")
llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.4, 
)

weatherdata = {
    "delhi": "33 degree",
    "hyderabad": "29 degree",
    "chennai": "28 degree"
}

class State(MessagesState):
    pass
    
graph = StateGraph(State)    
@tool
def multiply(a: float, b: float)-> float:
    """Multiply the variables a and b"""
    
    return a * b 

@tool
def cityweather(city: str)-> str:
    """Finding City Weather"""
    
    return weatherdata[city]

llm_with_tools = llm.bind_tools([multiply, cityweather])

def llm_node(state: State):
    
    response = llm_with_tools.invoke(state["messages"])
    
    return {"messages": [response]}
 
graph.add_node("llm", llm_node)
graph.add_node("tools", ToolNode([multiply, cityweather]))

graph.add_edge(START, "llm")

graph.add_conditional_edges(
    "llm",
    tools_condition
)

graph.add_edge("tools", "llm")

app = graph.compile()

from langchain_core.messages import HumanMessage

result = app.invoke({
    "messages": [
        HumanMessage(content="What is the weather in Hyderabad?")
    ]
})

print(result["messages"][-1].content)