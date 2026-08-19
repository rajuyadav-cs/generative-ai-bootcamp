from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from typing import TypedDict
from IPython.display import Image, display

load_dotenv()
prompt = PromptTemplate.from_template("Answer the topic: {topic}")
llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.4, 
)

class Answer(TypedDict):
    summary : str
    confidence : float
    
structured_llm = llm.with_structured_output(Answer)
chain = prompt | structured_llm

class State(TypedDict):
    topic: str
    answer: Answer
         
def llm_node(state: State):
    # print(state["answer"])
    
    response = chain.invoke({
        "topic": state["topic"]
    })
    # print(response)
    
    return {
        "answer": response
    }

graph = StateGraph(State)

graph.add_node("llm_node", llm_node)

graph.add_edge(START, "llm_node")
graph.add_edge("llm_node", END)

app = graph.compile()    

# print(display(Image(app.get_graph().draw_mermaid_png())))

result = app.invoke({
    "topic": "Artificial Intelligence",
    "answer":{
        "confidence":0.0,
        "summary":"Welcome to AlfansoGPT"
    }
})

print(result["answer"]["summary"])
