# Two-Stage Retrieval with Cross-Encoder Reranking
# ---------------------------------------------------
# Stage 1: Fast Bi-Encoder / Vector Search retrieves top candidate chunks (e.g. top 5).
# Stage 2: Cross-Encoder evaluates (Query, Document) pairs together for high-accuracy scoring.
# Stage 3: Top reranked chunks are passed to the LLM.

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from sentence_transformers import CrossEncoder

load_dotenv()

BI_ENCODER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ---------------------------------------------------
# STEP 1: Sample Documents
# ---------------------------------------------------

documents = [
    Document(
        page_content="Python is an interpreted programming language created by Guido van Rossum in 1991.",
        metadata={"id": "doc_1"}
    ),
    Document(
        page_content="To speed up Python execution, developers use PyPy, Cython, or Numba compiled C code.",
        metadata={"id": "doc_2"}
    ),
    Document(
        page_content="CPython uses the Global Interpreter Lock (GIL) to synchronize thread execution.",
        metadata={"id": "doc_3"}
    ),
    Document(
        page_content="Multiprocessing in Python bypasses the GIL by creating independent OS processes with separate memory spaces.",
        metadata={"id": "doc_4"}
    ),
    Document(
        page_content="The Python snake is a nonvenomous reptile native to tropical regions of Africa and Asia.",
        metadata={"id": "doc_5"}
    )
]

# ---------------------------------------------------
# STEP 2: Chroma Vector Store Setup (Stage 1)
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(model_name=BI_ENCODER_MODEL)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="reranking_demo"
)

# ---------------------------------------------------
# STEP 3: Stage 1 - Candidate Retrieval
# ---------------------------------------------------

query = "How can you run CPU-bound code in parallel in Python despite the GIL?"

print("\nQUERY:", query)
print("=" * 60)

# Retrieve top 4 candidates with Bi-Encoder vector search
candidates = vectorstore.similarity_search_with_score(query, k=4)

print("\nSTAGE 1: Bi-Encoder Candidate Results:")
for rank, (doc, score) in enumerate(candidates, 1):
    print(f"Rank #{rank} [Distance: {score:.4f}] [{doc.metadata['id']}]: {doc.page_content}")

# ---------------------------------------------------
# STEP 4: Stage 2 - Cross-Encoder Reranking
# ---------------------------------------------------

reranker = CrossEncoder(CROSS_ENCODER_MODEL)

# Prepare (Query, Document Content) pairs
pairs = [(query, doc.page_content) for doc, _ in candidates]
rerank_scores = reranker.predict(pairs)

# Combine and sort candidates by cross-encoder score descending
reranked_results = []
for (doc, initial_score), cross_score in zip(candidates, rerank_scores):
    reranked_results.append({
        "doc": doc,
        "initial_distance": initial_score,
        "cross_score": float(cross_score)
    })

reranked_results.sort(key=lambda x: x["cross_score"], reverse=True)

print("\n" + "=" * 60)
print("STAGE 2: Cross-Encoder Reranked Results:")
print("=" * 60)

for rank, item in enumerate(reranked_results, 1):
    doc = item["doc"]
    print(f"Rerank #{rank} [Cross-Encoder Score: {item['cross_score']:+.4f}] [{doc.metadata['id']}]:")
    print(f"{doc.page_content}\n")

# ---------------------------------------------------
# STEP 5: Generate Answer Using Top Reranked Document
# ---------------------------------------------------

top_docs = [item["doc"].page_content for item in reranked_results[:2]]
context = "\n\n".join(top_docs)

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

print("=" * 60)
print("FINAL ANSWER:")
print("=" * 60)
print(response.content)
