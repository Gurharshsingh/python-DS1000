import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# llm = ChatOllama(model="tinyllama:latest", temperature=0.7)



# 1. Load the OpenRouter API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Initialize the OpenRouter LLM
llm = ChatOpenAI(
    model_name="openrouter/free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7
)



# template = PromptTemplate.from_template("Explain the topic {topic}")
# formatted_message = template.format(topic = "Machine Learning")


# response = llm.invoke(formatted_message)
# print(response.content)



chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert tutor in {subject}. Keep your response {tone}."),
    ("human", "Explain {question}")
])

formatted_messages = chat_template.format_messages(
    subject="Python",
    tone="Angry",
    question="Why do we use AI?"
)


response = llm.invoke(formatted_messages)
print(response)



























# template = PromptTemplate.from_template("Give me one line definition on the topic {topic}")
# formatted_message = template.format(topic="Ollama")
# response = llm.invoke(formatted_message)
# print(response.content)



# print("\n--- 2. ChatPromptTemplate ---")
# chat_template = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert tutor in {subject}. Keep your response {tone}."),
#     ("human", "Explain {question}")
# ])

# # Format the template into a list of message objects
# formatted_messages = chat_template.format_messages(
#     subject="History",
#     tone="funny",
#     question="Why did the Roman Empire fall?"
# )