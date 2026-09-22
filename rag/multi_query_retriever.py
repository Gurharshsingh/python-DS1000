# Multi-Query Retriever in RAG (Query Expansion)
# ---------------------------------------------------
# Distance-based search can fail if the user's question misses keywords
# or takes only one narrow perspective.
#
# Solution:
# 1. Use LLM to generate multiple alternative versions of the question.
# 2. Run vector search for every query variation.
# 3. Combine and deduplicate the retrieved documents (Union).
# 4. Generate the final answer using the combined context.

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
# STEP 1: Sample Documents
# ---------------------------------------------------

documents = [
    Document(
        page_content="Quantum computers utilize qubits capable of superposition, enabling simultaneous parallel computation.",
        metadata={"source": "quantum_physics.txt"}
    ),
    Document(
        page_content="Shor's algorithm provides exponential speedup for factoring large integers, breaking RSA cryptography.",
        metadata={"source": "quantum_algorithms.txt"}
    ),
    Document(
        page_content="Grover's algorithm provides quadratic speedup for searching unsorted databases in O(sqrt(N)) steps.",
        metadata={"source": "quantum_algorithms.txt"}
    ),
    Document(
        page_content="Classical computers use silicon transistors and binary bits (0 or 1) inside Von Neumann architectures.",
        metadata={"source": "classical_computing.txt"}
    )
]

# ---------------------------------------------------
# STEP 2: Chroma Vector Store Setup
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="multi_query_demo"
)

# ---------------------------------------------------
# STEP 3: Setup LLM
# ---------------------------------------------------

api_key = os.getenv("OPEN_API_KEY")
if api_key:
    llm = ChatOpenAI(
        model_name="openrouter/free",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.3
    )
else:
    llm = ChatOllama(model="llama3.2:latest", temperature=0.3)

# ---------------------------------------------------
# STEP 4: Generate Query Variations (Expansion)
# ---------------------------------------------------

user_query = "How do quantum algorithms solve hard problems faster?"

prompt_variations = f"""Generate 3 different search questions based on the question below to search a vector database.
Output ONLY the questions, one per line:

Question: {user_query}
"""

response_queries = llm.invoke(prompt_variations)
generated_lines = [q.strip().lstrip("123.-) ") for q in response_queries.content.strip().split("\n") if q.strip()]

all_queries = [user_query] + generated_lines[:3]

print("\n--- GENERATED QUERY VARIATIONS ---")
for i, q in enumerate(all_queries):
    label = "Original" if i == 0 else f"Variant #{i}"
    print(f"[{label}]: {q}")

# ---------------------------------------------------
# STEP 5: Retrieve and Deduplicate (Union)
# ---------------------------------------------------

unique_docs = {}

for q in all_queries:
    results = vectorstore.similarity_search(q, k=2)
    for doc in results:
        unique_docs[doc.page_content] = doc

print(f"\nTotal Unique Documents Retrieved: {len(unique_docs)}")
print("=" * 60)

for idx, doc in enumerate(unique_docs.values(), 1):
    print(f"\nDocument #{idx} [{doc.metadata['source']}]:")
    print(doc.page_content)

# ---------------------------------------------------
# STEP 6: Generate Final Synthesized Answer
# ---------------------------------------------------

context = "\n\n".join([doc.page_content for doc in unique_docs.values()])

final_prompt = f"""Answer the question thoroughly based ONLY on the context below:

Context:
{context}

Question:
{user_query}
"""

final_answer = llm.invoke(final_prompt)

print("\n" + "=" * 60)
print("FINAL ANSWER:")
print("=" * 60)
print(final_answer.content)
