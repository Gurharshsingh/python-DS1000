import sys
import os
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationBufferMemory,ConversationSummaryMemory, ConversationTokenBufferMemory 
from langchain_classic.chains import ConversationChain 



# 1. Load the OpenRouter API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Initialize the OpenRouter LLM
llm = ChatOpenRouter(
    model="openrouter/free", 
    temperature=0.7,
    openrouter_api_key=api_key
)

# llm= ChatOllama(model='gemma3:1b')


# memory = ConversationBufferMemory()
# memory = ConversationSummaryMemory(llm=llm)
memory = ConversationTokenBufferMemory(llm= llm, max_token_limit=1500)


chatbot = ConversationChain(llm=llm, memory=memory)



while True:
    user_input = input("User: ")
    if user_input =="exit":
        print("Memory:", memory.load_memory_variables({}))
        break
    response = chatbot.predict(input = user_input)
    print("AI: ", response)
    print("Enter 'exit' to leave.")












# memory = ConversationBufferMemory()
# memory = ConversationSummaryMemory(llm = llm)
# memory = ConversationTokenBufferMemory(llm = llm, max_token_limit=500)

# chatbot = ConversationChain(llm= llm, memory = memory)

# while True:
#     user_input = input("User: ")
#     if user_input == 'exit':
#         print("Memory: ",memory.load_memory_variables({}))
#         break

#     response = chatbot.predict(input=user_input)
#     print("AI:",response)
















