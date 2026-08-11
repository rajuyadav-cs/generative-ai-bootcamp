from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from pydantic import BaseModel , Field
load_dotenv()

model = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.5,
    max_tokens = 100,   
)

# ----------Structured Output-------------

# creating a structure
class Person(BaseModel):
    name: str= Field(default= None, description= "Person's name")
    age: int = Field(default= None, description="Person's age")

structured_model = model.with_structured_output(Person)
response1 = structured_model.invoke("My name is Ruuh and I am 22 years old") 
response2 = model.invoke("Hii I am ruuh!")

# ------------Output Parsing------------
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
result = parser.invoke(response2)
# print(result)