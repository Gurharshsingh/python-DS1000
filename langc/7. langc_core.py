from langchain_ollama import ChatOllama

# Initialize the ChatOllama model (requires Ollama running locally)
llm = ChatOllama(
    model="tinyllama:latest",
    temperature=0.7
)

# Call the model directly
response = llm.invoke("how are you")
print(response.content)
