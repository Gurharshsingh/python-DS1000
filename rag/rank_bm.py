from rank_bm25 import BM25Okapi

data = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?",
    "Its quite windy in London and america",
    "It is not windy in Australia"
]

tokenized_data = [doc.split(" ") for doc in data]
print(tokenized_data)


bm25 = BM25Okapi(tokenized_data)

query = "windy london"
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)

print(doc_scores)

for doc , score in zip(data,doc_scores):
    print(f"Doc: {doc} | Score: {score}")


print(bm25.get_top_n(tokenized_query,data,n=1))

