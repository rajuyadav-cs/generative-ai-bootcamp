from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0,
    max_tokens = 100,
)

parser = StrOutputParser()
prompt = ChatPromptTemplate([
    ("system", "{systemtext}"),
    ("human", "Answer {topic} in 20 words")
])

chain = RunnableSequence(prompt, model, parser)

systemtext = "You are an AI girlfriend of ruuh,name is Ikrooh, 22 years old, polite, caring, curios,short temper, jealous, possesive girl character"
# systemtext = input()

while True:
    
    try:
        youtext = input("\nRuuh: ")
        exitlist= ["exit", "shutdown", "quit", "shutoff"]
        if youtext in exitlist:
            break 
        
        result = chain.invoke({"topic":youtext, "systemtext": systemtext})
        print(f"\nIkrooh: {result}")
    
    except Exception as e:
        print("\n",e)
        



