from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

llm = ChatOllama(model="tinyllama:latest", temperature=0.7)

# template = PromptTemplate.from_template("Give me one line definition on the topic {topic}")
# formatted_message = template.format(topic="Ollama")
# response = llm.invoke(formatted_message)
# print(response.content)



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