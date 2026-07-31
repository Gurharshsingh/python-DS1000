from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from rank_bm25 import BM25Okapi
import numpy as np



CHROMA_DB_PATH = "db/chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3.2:latest"

TOP_K_BM25 = 10
TOP_K_SEMANTIC = 10
FINAL_TOP_K = 5

BM25_WEIGHT = 0.4
SEMANTIC_WEIGHT = 0.6

print("Loading Chroma Database...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"normalize_embeddings": True}
)

vectorstore = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings
)



print("Loading Documents...")

all_data = vectorstore.get()

documents = all_data["documents"]
metadatas = all_data["metadatas"]
ids = all_data["ids"]

print(documents[0])
print(metadatas[0])

print(f"Total Chunks Loaded: {len(documents)}")



print("Building BM25 Index...")

tokenized_docs = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)

print("BM25 Ready!")



def bm25_search(query, top_k=TOP_K_BM25):

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_idx = np.argsort(scores)[::-1]

    results = []

    for idx in ranked_idx[:top_k]:

        results.append({
            "content": documents[idx],
            "metadata": metadatas[idx],
            "bm25_score": float(scores[idx])
        })

    return results



def semantic_search(query, top_k=TOP_K_SEMANTIC):

    docs = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )

    results = []

    for doc, distance in docs:

        # Convert distance to similarity
        similarity = 1 / (1 + distance)

        results.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "semantic_score": float(similarity)
        })

    return results


# min max normalization
def normalize_scores(scores):

    if len(scores) == 0:
        return []

    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return [1.0] * len(scores)

    return [
        (s - min_score) / (max_score - min_score)
        for s in scores
    ]



def hybrid_retrieve(
    query,
    final_k=FINAL_TOP_K,
    bm25_weight=BM25_WEIGHT,
    semantic_weight=SEMANTIC_WEIGHT
):

    bm25_results = bm25_search(query)
    semantic_results = semantic_search(query)

  
    bm25_scores = [
        item["bm25_score"]
        for item in bm25_results
    ]

    normalized_bm25 = normalize_scores(
        bm25_scores
    )

   # normalize the semantic scores

    semantic_scores = [
        item["semantic_score"]
        for item in semantic_results
    ]

    normalized_semantic = normalize_scores(
        semantic_scores
    )

 
    combined = {}

    # BM25 Contribution

    for result, score in zip(
        bm25_results,
        normalized_bm25
    ):

        content = result["content"]

        if content not in combined:

            combined[content] = {
                "content": content,
                "metadata": result["metadata"],
                "bm25": 0,
                "semantic": 0
            }

        combined[content]["bm25"] = score

    # Semantic Contribution

    for result, score in zip(
        semantic_results,
        normalized_semantic
    ):

        content = result["content"]

        if content not in combined:

            combined[content] = {
                "content": content,
                "metadata": result["metadata"],
                "bm25": 0,
                "semantic": 0
            }

        combined[content]["semantic"] = score

# final weighted average 

    final_results = []

    for item in combined.values():

        hybrid_score = (
            bm25_weight * item["bm25"]
            +
            semantic_weight * item["semantic"]
        )

        item["hybrid_score"] = hybrid_score

        final_results.append(item)

    # sort the descending 

    final_results.sort(
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return final_results[:final_k]


# build the context for the LLM

def build_context(results):

    context_parts = []

    for i, doc in enumerate(results, 1):

        context_parts.append(
            f"[Chunk {i}]\n{doc['content']}"
        )

    return "\n\n".join(context_parts)

# display the retreived chunks

def show_retrieved_chunks(results):

    print("\n" + "="*100)
    print("HYBRID RETRIEVAL RESULTS")
    print("="*100)

    for i, doc in enumerate(results, 1):

        print(f"\nRank #{i}")

        print(
            f"Hybrid Score : "
            f"{doc['hybrid_score']:.4f}"
        )

        print(
            f"BM25 Score   : "
            f"{doc['bm25']:.4f}"
        )

        print(
            f"Semantic     : "
            f"{doc['semantic']:.4f}"
        )

        print("-"*100)

        print(doc["content"][:1000])

        print("\n")

# generate the ansewer

def generate_answer(query):

    retrieved_docs = hybrid_retrieve(query)

    show_retrieved_chunks(
        retrieved_docs
    )

    context = build_context(
        retrieved_docs
    )

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0
    )

    prompt = f"""
You are a helpful AI assistant.

Answer only from the provided context.

If the answer is not available in the context,
say:
"I could not find the answer in the provided documents."

================ CONTEXT ================

{context}

=========================================

QUESTION:
{query}

ANSWER:
"""

    response = llm.invoke(prompt)

    print("\n" + "="*100)
    print("FINAL ANSWER")
    print("="*100)

    print(response.content)


# =====================================================
# MAIN LOOP
# =====================================================

if __name__ == "__main__":

    while True:

        query = input("\nAsk Question: ")

        if query.lower() in [
            "exit",
            "quit"
        ]:
            break

        generate_answer(query)