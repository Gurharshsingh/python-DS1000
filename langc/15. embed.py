from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

q='Langchain is the framework that is used in genrative ai.'
docs=[
    'Raman is very good boy',
    'He is from Hoshiarpur',
    'He is 22 years old'
]
# embedder=OllamaEmbeddings(model='qwen3-embedding:0.6b')
# embedder=OllamaEmbeddings(model='nomic-embed-text:latest')
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# vector1= embedder.embed_query(q)
# print(vector1)
# print(f"Dimension of vector {len(vector1)}")
vector2= embedder.embed_documents(docs)
# print(vector2)
for i in vector2:
    print("--"*10)
    print(i)
print(f"Dimension of vector {len(vector2)}")

