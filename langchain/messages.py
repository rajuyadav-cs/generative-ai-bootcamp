from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()
# ---------------initializing the llm's--------------

llm = init_chat_model(
    model= os.getenv("MODEL"),
    model_provider= os.getenv("PROVIDER"),
    max_tokens = 100,
    temperature = 0.3
    )

def startLLM():
    
    try: 
        
        while True:
            
            text = input("\nYOU: ")
            text = text.lower()
            system_text = "You are my girlfriend who is 22 years old ,who really care about ruuh so much , possessive and jealous always"
            
            messages = [
                HumanMessage(text),
                SystemMessage(system_text)
            ]
            
            if text == 'quit':
                break 
            response = llm.invoke(messages).content 
            print(f"\nSystem: {response}")
    
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    
    startLLM()        