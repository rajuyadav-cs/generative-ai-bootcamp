from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()




def startLLM():
    
    try: 
        llm = init_chat_model(
            model= os.getenv("MODEL"),
            model_provider= os.getenv("PROVIDER"),
            max_tokens = 100,
            temperature = 0.3
            )
        prompt = PromptTemplate.from_template("Explain {text} in simple word as a patient teacher")
        
        while True:
            
            text = input("\nYOU: ")
            text = text.lower()
            
            
            if text == 'quit':
                break 
            formated_prompt = prompt.invoke({"text": text})
            response = llm.invoke(formated_prompt).content
            print(f"\nSystem: {response}")
    
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    
    startLLM()  