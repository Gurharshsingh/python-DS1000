# Hybrid Search using BM25 + Semantic Search
# -----------------------------------------
# Install:
# pip install rank-bm25 sentence-transformers scikit-learn numpy

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---------------------------------------------------
# STEP 1: Sample Documents
# ---------------------------------------------------

documents = [
    "Python is a programming language used for AI and web development.",
    "Machine learning is a subset of artificial intelligence.",
    "The Taj Mahal is one of the seven wonders of the world.",
    "Deep learning uses neural networks for complex tasks.",
    "Cricket is one of the most popular sports in India.",
    "Artificial intelligence is transforming healthcare and education."
]

# ---------------------------------------------------
# STEP 2: BM25 Setup (Keyword Search)
# ---------------------------------------------------

tokenized_docs = [doc.lower().split() for doc in documents]

bm25 = BM25Okapi(tokenized_docs)

# ---------------------------------------------------
# STEP 3: Semantic Search Setup
# ---------------------------------------------------

model = SentenceTransformer('all-MiniLM-L6-v2')

doc_embeddings = model.encode(documents)

# ---------------------------------------------------
# STEP 4: User Query
# ---------------------------------------------------

query = "AI applications in healthcare"

# ---------------------------------------------------
# STEP 5: BM25 Scores
# ---------------------------------------------------

tokenized_query = query.lower().split()

bm25_scores = bm25.get_scores(tokenized_query)

# Normalize BM25 scores
bm25_scores = np.array(bm25_scores)  #
bm25_scores = bm25_scores / bm25_scores.max()

# ---------------------------------------------------
# STEP 6: Semantic Similarity Scores
# ---------------------------------------------------

query_embedding = model.encode([query])

semantic_scores = cosine_similarity(
    query_embedding,
    doc_embeddings
)[0]

# Normalize semantic scores (Min max Scaling )
semantic_scores = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min())

# ---------------------------------------------------
# STEP 7: Hybrid Score Combination
# ---------------------------------------------------

alpha = 0.5 # 0.5 → equal weight to BM25 and semantic scores

hybrid_scores = (
    alpha * bm25_scores
    + (1 - alpha) * semantic_scores
)

# ---------------------------------------------------
# STEP 8: Rank Results
# ---------------------------------------------------

ranked_results = sorted(
    zip(documents, hybrid_scores, bm25_scores, semantic_scores),
    key=lambda x: x[1],
    reverse=True
)

# ---------------------------------------------------
# STEP 9: Display Results
# ---------------------------------------------------

print("\nQUERY:", query)
print("\nTop Results:\n")

for idx, (doc, hybrid, bm25_s, sem_s) in enumerate(ranked_results, start=1):
    print(f"Rank {idx}")
    print(f"Document : {doc}")
    print(f"Hybrid   : {hybrid:.4f}")
    print(f"BM25      : {bm25_s:.4f}")
    print(f"Semantic  : {sem_s:.4f}")
    print("-" * 60)
