# Parent Document Retriever in RAG
# ---------------------------------------------------
# Small chunks = high search precision, but lack context for LLM.
# Large chunks = rich LLM context, but poor search precision.
#
# Solution:
# Index small child chunks for search, but retrieve the full parent chunk for the LLM.

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.stores import InMemoryStore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------
# STEP 1: Sample Documents (Longer context)
# ---------------------------------------------------

documents = [
    Document(
        page_content="""The Mars 2020 mission features NASA's Perseverance rover exploring Jezero Crater. 
Jezero Crater was chosen because it was once flooded with water and home to an ancient river delta. 
One prominent payload is MOXIE (Mars Oxygen ISRU Experiment), which produces breathable oxygen 
directly from the atmospheric carbon dioxide on Mars to support future human missions.""",
        metadata={"source": "mars_mission.txt"}
    ),
    Document(
        page_content="""The Transformer architecture was introduced in 2017 in the paper 'Attention Is All You Need'. 
It replaces recurrence with self-attention mechanisms, allowing tokens in a sentence to be processed 
in parallel. Scaled Dot-Product Attention computes relationships across all tokens simultaneously, 
forming the backbone of models like BERT, GPT, and LLaMA.""",
        metadata={"source": "transformers.txt"}
    )
]

# ---------------------------------------------------
# STEP 2: Configure Parent and Child Splitters
# ---------------------------------------------------

# Parent splitter creates larger chunks for the LLM
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0)

# Child splitter creates small chunks for vector search
child_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)

# ---------------------------------------------------
# STEP 3: Setup Storage and Retriever
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Chroma stores child chunk vector embeddings
vectorstore = Chroma(
    collection_name="parent_retriever_demo",
    embedding_function=embeddings
)

# InMemoryStore stores the full parent documents
docstore = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

retriever.add_documents(documents)

print("\nIndexed Documents:")
print(f"Parent Chunks in DocStore: {len(list(docstore.yield_keys()))}")
print(f"Child Chunks in Chroma   : {len(vectorstore.get()['ids'])}")

# ---------------------------------------------------
# STEP 4: Query and Comparison
# ---------------------------------------------------

query = "What is MOXIE and what does it do on Mars?"

print("\nQUERY:", query)
print("=" * 60)

# What vector search matches (Child Chunk):
print("\n1. SMALL CHILD CHUNK (Matched by Vector Store):")
child_doc = vectorstore.similarity_search(query, k=1)[0]
print(f"Length: {len(child_doc.page_content)} chars")
print(f"Content: \"{child_doc.page_content}\"")

# What ParentDocumentRetriever returns (Full Parent Chunk):
print("\n" + "=" * 60)
print("2. PARENT CHUNK RETURNED (Restored full context for LLM):")
parent_docs = retriever.invoke(query)
for i, doc in enumerate(parent_docs, 1):
    print(f"\nParent #{i} ({len(doc.page_content)} chars):")
    print(doc.page_content)

# ---------------------------------------------------
# STEP 5: Generate Answer with Parent Context
# ---------------------------------------------------

context = "\n\n".join([doc.page_content for doc in parent_docs])

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

print("\n" + "=" * 60)
print("FINAL ANSWER:")
print("=" * 60)
print(response.content)
