"""
=============================================================================
ChromaDB Vector Store Example (AI-native Embedded Vector DB)
=============================================================================
Chroma is a popular open-source, AI-native vector database designed to make 
it easy to build LLM apps with embeddings.

Key Features:
- Built-in persistence to disk (DuckDB/SQLite + Parquet under the hood)
- Rich metadata filtering (filter by tags, categories, timestamps)
- Simple setup without running complex server infrastructure
- Great developer experience & seamless LangChain integration
=============================================================================
"""

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# 1. Initialize the Embedding Model
print("--> Loading embedding model...")
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Prepare Sample Documents with Metadata
sample_docs = [
    Document(page_content="LangChain makes it easy to connect LLMs with custom vector databases.", metadata={"category": "ai", "year": 2024}),
    Document(page_content="Chroma is an open-source embedding database built for AI applications.", metadata={"category": "database", "year": 2023}),
    Document(page_content="Python is used widely across machine learning and data science workflows.", metadata={"category": "programming", "year": 2024}),
    Document(page_content="Vector databases store embeddings to enable semantic similarity searches.", metadata={"category": "database", "year": 2024}),
]

persist_directory = "db/chroma_db"

# 3. Create and Persist Chroma Vector Store
print(f"--> Creating Chroma DB with persistence at '{persist_directory}'...")
vector_db = Chroma.from_documents(
    documents=sample_docs,
    embedding=embedder,
    persist_directory=persist_directory,
    collection_name="my_documents"
)
print("--> Chroma DB created and saved successfully!")

# 4. Load Existing Chroma Vector Store from Disk
loaded_db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedder,
    collection_name="my_documents"
)
print("--> Chroma DB loaded from disk successfully!")

# 5. Simple Similarity Search
query = "What database is designed for embeddings and AI?"
print(f"\n[Query]: {query}\n" + "-"*50)

results = loaded_db.similarity_search(query, k=2)
for i, doc in enumerate(results, 1):
    print(f"Result {i}:")
    print(f"  Content : {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")

# 6. Similarity Search with Metadata Filtering
print("\n[Search with Metadata Filter (category = 'database')]:\n" + "-"*50)
filtered_results = loaded_db.similarity_search(
    query, 
    k=2, 
    filter={"category": "database"}
)
for i, doc in enumerate(filtered_results, 1):
    print(f"Result {i}:")
    print(f"  Content : {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")

# 7. Similarity Search with Relevance Score (Cosine distance)
print("\n[Search with Relevance Score]:\n" + "-"*50)
results_with_score = loaded_db.similarity_search_with_score(query, k=2)
for doc, score in results_with_score:
    print(f"  Score ({score:.4f}): {doc.page_content}")
