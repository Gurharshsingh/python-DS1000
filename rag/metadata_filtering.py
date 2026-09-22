# Metadata Filtering in Vector Retrieval
# ---------------------------------------------------
# Metadata filtering restricts semantic vector search using structured attributes
# like category, topic, year, author, or document type.
#
# Supported Chroma Filter Operators:
#   1. Exact Match:          {"topic": "space"}
#   2. Not Equal ($ne):       {"topic": {"$ne": "ai"}}
#   3. Greater/Equal ($gte):  {"year": {"$gte": 2024}}
#   4. Less Than ($lt):       {"year": {"$lt": 2024}}
#   5. In List ($in):         {"author": {"$in": ["NASA", "SpaceX"]}}
#   6. Not In List ($nin):    {"author": {"$nin": ["OpenAI"]}}
#   7. Logical AND ($and):    {"$and": [{"topic": "ai"}, {"year": {"$gte": 2023}}]}
#   8. Logical OR ($or):      {"$or": [{"topic": "space"}, {"doc_type": "paper"}]}

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------
# STEP 1: Sample Documents with Rich Metadata
# ---------------------------------------------------

documents = [
    Document(
        page_content="NASA's Artemis program aims to land astronauts on the Moon by 2026.",
        metadata={"topic": "space", "year": 2024, "author": "NASA", "doc_type": "report"}
    ),
    Document(
        page_content="SpaceX Starship is designed for cargo and crew missions to Mars.",
        metadata={"topic": "space", "year": 2023, "author": "SpaceX", "doc_type": "article"}
    ),
    Document(
        page_content="James Webb Space Telescope observes the earliest galaxies using infrared sensors.",
        metadata={"topic": "space", "year": 2022, "author": "NASA", "doc_type": "paper"}
    ),
    Document(
        page_content="Convolutional Neural Networks (CNNs) are widely used for computer vision and medical imaging.",
        metadata={"topic": "ai", "year": 2023, "author": "DeepMind", "doc_type": "paper"}
    ),
    Document(
        page_content="Large Language Models use transformer architectures with multi-head self-attention.",
        metadata={"topic": "ai", "year": 2024, "author": "OpenAI", "doc_type": "paper"}
    ),
    Document(
        page_content="Mars rovers use computer vision and reinforcement learning for autonomous navigation.",
        metadata={"topic": "ai", "year": 2023, "author": "NASA", "doc_type": "report"}
    )
]

# ---------------------------------------------------
# STEP 2: Chroma Vector Store Setup
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="metadata_filter_demo"
)

# ---------------------------------------------------
# STEP 3: User Query
# ---------------------------------------------------

query = "What systems use computer vision or advanced technology to explore or diagnose?"

print("\nQUERY:", query)
print("=" * 65)

# Helper function to print search results
def print_results(filter_name, results):
    print(f"\n{filter_name}")
    print("-" * 65)
    if not results:
        print("  (No documents matched)")
        return
    for rank, (doc, score) in enumerate(results, 1):
        print(f"Rank {rank} [Score: {score:.4f} | Meta: {doc.metadata}]")
        print(f"Content: {doc.page_content}\n")

# ---------------------------------------------------
# FILTER 1: Unfiltered Search
# ---------------------------------------------------
res_unfiltered = vectorstore.similarity_search_with_score(query, k=3)
print_results("1. UNFILTERED SEARCH (No metadata constraints):", res_unfiltered)

# ---------------------------------------------------
# FILTER 2: Exact Match (topic == 'space')
# ---------------------------------------------------
filter_exact = {"topic": "space"}
res_exact = vectorstore.similarity_search_with_score(query, k=2, filter=filter_exact)
print_results("2. EXACT MATCH FILTER (topic == 'space'):", res_exact)

# ---------------------------------------------------
# FILTER 3: Not Equal ($ne: exclude 'ai')
# ---------------------------------------------------
filter_ne = {"topic": {"$ne": "ai"}}
res_ne = vectorstore.similarity_search_with_score(query, k=2, filter=filter_ne)
print_results("3. NOT-EQUAL FILTER ($ne: topic != 'ai'):", res_ne)

# ---------------------------------------------------
# FILTER 4: Comparison ($gte: year >= 2024)
# ---------------------------------------------------
filter_gte = {"year": {"$gte": 2024}}
res_gte = vectorstore.similarity_search_with_score(query, k=2, filter=filter_gte)
print_results("4. COMPARISON FILTER ($gte: year >= 2024):", res_gte)

# ---------------------------------------------------
# FILTER 5: List Membership ($in: author in ['NASA', 'SpaceX'])
# ---------------------------------------------------
filter_in = {"author": {"$in": ["NASA", "SpaceX"]}}
res_in = vectorstore.similarity_search_with_score(query, k=2, filter=filter_in)
print_results("5. IN-LIST FILTER ($in: author in ['NASA', 'SpaceX']):", res_in)

# ---------------------------------------------------
# FILTER 6: Logical OR ($or: topic == 'space' OR doc_type == 'paper')
# ---------------------------------------------------
filter_or = {
    "$or": [
        {"topic": "space"},
        {"doc_type": "paper"}
    ]
}
res_or = vectorstore.similarity_search_with_score(query, k=3, filter=filter_or)
print_results("6. LOGICAL OR FILTER ($or: topic == 'space' OR doc_type == 'paper'):", res_or)

# ---------------------------------------------------
# FILTER 7: Compound AND with Range ($and: topic == 'ai' AND year >= 2023)
# ---------------------------------------------------
filter_and = {
    "$and": [
        {"topic": "ai"},
        {"year": {"$gte": 2023}}
    ]
}
res_and = vectorstore.similarity_search_with_score(query, k=2, filter=filter_and)
print_results("7. COMPOUND AND FILTER ($and: topic == 'ai' AND year >= 2023):", res_and)

# ---------------------------------------------------
# STEP 4: Answer Generation with Filtered Context
# ---------------------------------------------------

# Using Filter 5 (Only NASA / SpaceX documents) for context
context = "\n".join([f"[{doc.metadata['author']} - {doc.metadata['year']}] {doc.page_content}" for doc, _ in res_in])

api_key = os.getenv("OPEN_API_KEY")
if api_key:
    llm = ChatOpenAI(
        model_name="openrouter/free",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.2
    )
else:
    llm = ChatOllama(model="llama3.2:latest", temperature=0.2)

prompt = f"""Answer the question based ONLY on the context below:

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print("=" * 65)
print("FINAL ANSWER (Generated from NASA/SpaceX filtered context):")
print("=" * 65)
print(response.content)
