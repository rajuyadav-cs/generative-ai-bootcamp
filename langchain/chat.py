from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
load_dotenv(r"D:\Programming\generative-ai-bootcamp\.env")

# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0.3,
#     max_tokens=200
# )

# ------------OR----------------
chatllm = init_chat_model(model="llama-3.3-70b-versatile", model_provider= "groq", temperature = 0,max_tokens = 100)

def getResponse(text):
    
    # response = llm.invoke(text)
    response = chatllm.invoke(text)
    return response.content

if __name__ == "__main__":
    
    try:
        while True:
            text = input("\nYou: ")
            text = text.lower()
            if text  == "quit":
                break
            
            response = getResponse(text)
            print(f"\nSystem: {response}")
    except Exception as e:
        print(f"Error: {e}")
                