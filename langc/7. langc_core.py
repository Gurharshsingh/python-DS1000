#pip install langchain-core
# pip install langchain-ollama

# from langchain_ollama import ChatOllama 



# llm  = ChatOllama(model = "llama3.2:latest",temperature = 0.6)


# response  = llm.invoke("Hello how r u?")

# print(response.content)


from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

llm  = ChatOpenRouter(model="nvidia/nemotron-3.5-lightning:free", openrouter_api_key=api_key)


response  = llm.invoke("hello")
print(response.content)