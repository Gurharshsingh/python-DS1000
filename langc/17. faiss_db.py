"""
=============================================================================
FAISS Vector Store Example (Facebook AI Similarity Search)
=============================================================================
FAISS is an open-source library developed by Meta (Facebook AI Research) 
for extremely fast similarity search and clustering of dense vectors.

Key Features:
- Super fast (C++ backend with Python wrapper, GPU support available)
- In-memory index (can be saved/loaded to/from disk)
- Ideal for quick prototyping, local experiments, and read-heavy similarity search
=============================================================================
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# 1. Initialize the Embedding Model
print("--> Loading embedding model...")
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Prepare Sample Documents
sample_docs = [
    Document(page_content="Python is a high-level programming language great for AI and data science.", metadata={"topic": "python"}),
    Document(page_content="LangChain provides tools to build LLM-powered applications and RAG pipelines.", metadata={"topic": "langchain"}),
    Document(page_content="FAISS is developed by Meta for lightning-fast dense vector similarity search.", metadata={"topic": "vector_db"}),
    Document(page_content="Machine learning models require good quality embeddings for semantic search.", metadata={"topic": "ml"}),
]

# 3. Create FAISS Vector Store from Documents
print("--> Creating FAISS index from documents...")
vector_db = FAISS.from_documents(documents=sample_docs, embedding=embedder)

# 4. Save the FAISS index to local disk
save_path = "db/faiss_index"
os.makedirs("db", exist_ok=True)
vector_db.save_local(save_path)
print(f"--> FAISS index saved successfully at '{save_path}'")

# 5. Load the FAISS index from local disk
# Note: allow_dangerous_deserialization is required when loading local pickle/index files
loaded_db = FAISS.load_local(
    folder_path=save_path, 
    embeddings=embedder, 
    allow_dangerous_deserialization=True
)
print("--> FAISS index reloaded from disk successfully!")

# 6. Perform Similarity Search
query = "Tell me about Meta's vector search tool"
print(f"\n[Query]: {query}\n" + "-"*50)

# Retrieve top 2 most relevant documents
results = loaded_db.similarity_search(query, k=2)

for i, doc in enumerate(results, 1):
    print(f"Result {i}:")
    print(f"  Content : {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")

# 7. Similarity Search with Relevance Score (L2 Distance: Lower score = closer match)
print("\n[Search with Score (L2 Distance)]:" + "\n" + "-"*50)
results_with_score = loaded_db.similarity_search_with_score(query, k=2)
for doc, score in results_with_score:
    print(f"  Score ({score:.4f}): {doc.page_content}")
