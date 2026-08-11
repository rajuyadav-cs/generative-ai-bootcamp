from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableSequence,
    RunnableParallel,
    RunnableLambda
)

load_dotenv()

# --------------------------------------------------
# Prompt Template
# --------------------------------------------------

formated_prompt = PromptTemplate.from_template(
    "Explain the {topic} in 50 words"
)

# --------------------------------------------------
# Chat Model
# --------------------------------------------------

model = init_chat_model(
    model=os.getenv("MODEL"),
    model_provider=os.getenv("PROVIDER"),
    temperature=0.3,
    max_tokens=1000,
)

parser = StrOutputParser()

# --------------------------------------------------
# LCEL / RunnableSequence
# --------------------------------------------------

chain = formated_prompt | model | parser

# print(chain.invoke({"topic": "python"}))


# --------------------------------------------------
# stream()
# --------------------------------------------------

formated_prompt1 = PromptTemplate.from_template(
    "Explain the {topic} in 10 words"
)

chain = formated_prompt1 | model | parser

# for chunk in chain.stream({"topic": "Langchain"}):
#     print(chunk, end="", flush=True)


# --------------------------------------------------
# batch()
# --------------------------------------------------

results = chain.batch([
    {"topic": "AI"},
    {"topic": "JAVA"},
    {"topic": "MACHINE LEARNING"}
])

for result in results:
    print(result)


# ==================================================
# 1. RunnableSequence
# ==================================================

sequence = RunnableSequence(
    formated_prompt1,
    model,
    parser
)

result = sequence.invoke({"topic": "Python"})

print("\n--- RunnableSequence ---")
print(result)


# ==================================================
# 2. RunnableParallel
# ==================================================

parallel = RunnableParallel(
    python=formated_prompt1 | model | parser,
    ai=PromptTemplate.from_template(
        "Define {topic} in 5 words"
    ) | model | parser
)

result = parallel.invoke({
    "topic": "Python"
})

print("\n--- RunnableParallel ---")
print(result)


# ==================================================
# 3. RunnableLambda
# ==================================================

def add_message(text):
    return f"AI says: {text}"


lambda_runnable = RunnableLambda(add_message)

lambda_chain = (
    formated_prompt1
    | model
    | parser
    | lambda_runnable
)

result = lambda_chain.invoke({
    "topic": "LangChain"
})

print("\n--- RunnableLambda ---")
print(result)