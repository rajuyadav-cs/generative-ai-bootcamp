from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent

load_dotenv()

weatherdata  = {
    "delhi": "34 degree",
    "hyderabad": "32 degree",
    "raipur": "43 degree",
    "nagpur": "12 degree"
}

@tool
def weathertool(city:str) -> str:
    """Weather data tool"""
    city = city.lower()
    
    return f"{city}-{weatherdata[city]}"

@tool
def add(a:float, b:float) -> float:
    """Addition tool"""
    
    return a + b 

# prompt = PromptTemplate.from_template("Answer {topic} in 50 words")
llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.5, 
    max_tokens = 1000, 
)

agent = create_agent(
    model= llm,
    tools= [add, weathertool]
)

# result = agent.invoke({
#     "messages": [
#         {"role": "user", "content": "What is the weather in delhi?"}
#     ]
# })

# print(result["messages"][-1].content)


# ------------------multiple calls using multiple tools in agents---------------
result = agent.invoke(
    {
        "messages":[
            {"role":"user", "content": "What is weather in hyderabad and 20 + 30 is??"},
        ]
    }
)

# for message in result["messages"]:
#     print(f"{type(message).__name__}")
#     print(message)
#     print("-"*50)

print(result["messages"][-1].content)