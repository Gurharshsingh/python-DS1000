import sys
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_ollama import ChatOllama

# Configure console stdout to handle Unicode/UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize ChatOllama LLM (make sure Ollama is running locally)
llm = ChatOllama(
    model="tinyllama:latest",
    temperature=0.7
)


# 1. Simple PromptTemplate Example (Without Chaining)
print("--- 1. Simple PromptTemplate ---")
template = PromptTemplate.from_template("Explain {topic} in one simple sentence.")

# Format the template into a raw string
formatted_prompt = template.format(topic="Quantum Physics")
print("Compiled Prompt:", formatted_prompt)

# Invoke the LLM directly with the string
response = llm.invoke(formatted_prompt)
print("LLM Response:", response.content)


# 2. ChatPromptTemplate Example (Without Chaining)
print("\n--- 2. ChatPromptTemplate ---")
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert tutor in {subject}. Keep your response {tone}."),
    ("human", "Explain {question}")
])

# Format the template into a list of message objects
formatted_messages = chat_template.format_messages(
    subject="History",
    tone="funny",
    question="Why did the Roman Empire fall?"
)

print("System Message:", formatted_messages[0].content)
print("User Message:", formatted_messages[1].content)

# Invoke the LLM directly with the list of messages
chat_response = llm.invoke(formatted_messages)
print("LLM Response:", chat_response.content)
