from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ToolMessage
load_dotenv()

prompt = PromptTemplate.from_template("Tell me {text} in 50 words")
# -----------LLM without TOOLS
llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    temperature = 0.3,
    max_tokens = 4096
)

# ----------LLM with TOOLS-----------------
@tool
def add(a:int, b:int)-> int:
    """Adding Two Integers"""
    return a + b 
@tool
def multiply(a:int, b:int)-> int:
    """Multiply Two Integers"""
    return a * b 

@tool
def weather(city:str)->str:
    """Getting the City Weather"""
    return "Sunny"
    

llm_tools = llm.bind_tools([add, multiply, weather])
parser = StrOutputParser()


# print(add.name)
# print(add.description)
# print(add.invoke({
#     "a":12,"b":22
# }))
# print(add)

# ------------------calling the model------------------
# chain = RunnableSequence(prompt, llm, parser)
chainwithtools = RunnableSequence(prompt, llm_tools)

# response = chain.invoke({"text":"What is 1111111111111+ 222222222222222??"})
# print(response)
# print("----------------------------------------")
# response1 = chainwithtools.invoke({"text":"What is 4546 * 343??"})
# tool_call = response1.tool_calls[0]
# result = multiply.invoke(tool_call["args"])
# tool_message = ToolMessage(
#     content= str(result),
#     tool_call_id = tool_call["id"]
# )

# final_response = llm_tools.invoke([response1, tool_message])

# print(final_response.content)


# ---------------------Multiple tool calls-----------------------

response2 = llm_tools.invoke(
    "What is 4 + 2 and 45 * 22?"
)

tools = {
    "add": add,
    "multiply": multiply,
    "weather": weather
}

tool_messages = []

for tool_call in response2.tool_calls:

    selected_tool = tools[tool_call["name"]]

    result = selected_tool.invoke(tool_call["args"])

    tool_messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )

final_response = llm_tools.invoke([
    response2,
    *tool_messages
])

print(final_response.content)