"""
=============================================================================
Qdrant Vector Store Example (Production-Ready Vector Database)
=============================================================================
Qdrant is an open-source, high-performance vector search engine written in Rust.
It provides production-ready vector similarity search with extensive payload 
(metadata) filtering and rich distance metrics.

Key Features:
- Written in Rust for maximum speed, memory safety, and high concurrency
- Advanced Payload Filtering (nested conditions, boolean logic, ranges)
- Can run: In-Memory (for quick testing), Local Disk (path), or Docker / Cloud
- Full CRUD operations with dynamic vector updates and deletions
=============================================================================
"""

import os
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from qdrant_client.http import models

# 1. Initialize the Embedding Model
print("--> Loading embedding model...")
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Prepare Sample Documents with Metadata / Payloads
sample_docs = [
    Document(page_content="Qdrant is written in Rust and built for high-performance vector search.", metadata={"category": "database", "speed": "high"}),
    Document(page_content="LangChain simplifies building RAG applications with vector databases.", metadata={"category": "framework", "speed": "medium"}),
    Document(page_content="Rust provides memory safety and concurrency without a garbage collector.", metadata={"category": "language", "speed": "ultra"}),
    Document(page_content="Vector embeddings turn unstructured text into numerical coordinates.", metadata={"category": "ai", "speed": "high"}),
]

# 3. Create Qdrant Vector Store
# Modes:
#   - location=":memory:" -> Fast in-memory mode for testing & prototyping
#   - path="db/qdrant_db" -> Local disk persistence (no Docker/server required)
#   - url="http://localhost:6333" -> Connect to running Qdrant Docker or Cloud
persist_path = "db/qdrant_db"
collection_name = "my_qdrant_collection"

print(f"--> Creating Qdrant Vector Store on local disk at '{persist_path}'...")
vector_db = QdrantVectorStore.from_documents(
    documents=sample_docs,
    embedding=embedder,
    path=persist_path,
    collection_name=collection_name
)
print("--> Qdrant Vector Store created successfully!")

# 4. Simple Similarity Search
query = "Tell me about the Rust vector database"
print(f"\n[Query]: {query}\n" + "-"*50)

results = vector_db.similarity_search(query, k=2)
for i, doc in enumerate(results, 1):
    print(f"Result {i}:")
    print(f"  Content : {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")

# 5. Similarity Search with Score (Cosine similarity: Higher score = closer match)
print("\n[Search with Score]:\n" + "-"*50)
results_with_score = vector_db.similarity_search_with_score(query, k=2)
for doc, score in results_with_score:
    print(f"  Score ({score:.4f}): {doc.page_content}")

# 6. Similarity Search with Payload/Metadata Filter (Qdrant models.Filter)
print("\n[Search with Metadata Filter (category = 'database')]:\n" + "-"*50)
category_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="metadata.category",
            match=models.MatchValue(value="database"),
        )
    ]
)

filtered_results = vector_db.similarity_search(
    query, 
    k=2, 
    filter=category_filter
)
for i, doc in enumerate(filtered_results, 1):
    print(f"Result {i}:")
    print(f"  Content : {doc.page_content}")
    print(f"  Metadata: {doc.metadata}")
