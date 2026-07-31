import os
from dotenv import load_dotenv

# LangChain components (from files 13-16 in langc)
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain_community.chat_models import ChatOpenAI

try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama

# Load environment variables (API Key if available)
load_dotenv()

DB_DIR = "db/chroma_db"
DOCS_DIR = "rag/sample_docs"

# -------------------------------------------------------------
# STEP 1: Document Loading (Reference: 13. documentload.py)
# -------------------------------------------------------------
def load_documents(docs_path=DOCS_DIR):
    """Loads all .txt documents from the given folder."""
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        print(f"Created folder '{docs_path}'. Please add text files to it.")
        return []

    loader = DirectoryLoader(docs_path, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s) from '{docs_path}'.")
    return documents

# -------------------------------------------------------------
# STEP 2: Text Splitting / Chunking (Reference: 14. textSplitter.py)
# -------------------------------------------------------------
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """Splits documents into smaller text chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunk(s).")
    return chunks

# -------------------------------------------------------------
# STEP 3: Vector Embedding & Storage (Reference: 15. embed.py & 16. ingestion_1.py)
# -------------------------------------------------------------
def create_vectorstore(chunks, db_directory=DB_DIR):
    """Embeds text chunks and stores them in Chroma Vector DB."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=db_directory)
    print(f"Vector store saved successfully at '{db_directory}'.")
    return vectorstore

def load_vectorstore(db_directory=DB_DIR):
    """Loads existing Chroma Vector DB."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    return Chroma(persist_directory=db_directory, embedding_function=embeddings)

# -------------------------------------------------------------
# STEP 4: Information Retrieval (Reference: retreive.py)
# -------------------------------------------------------------
def retrieve_context(query, vectorstore, k=3):
    """Searches vector store for top k relevant text chunks."""
    results = vectorstore.similarity_search(query=query, k=k)
    context = ""
    for i, doc in enumerate(results, start=1):
        context += f"\n--- Chunk {i} ---\n{doc.page_content}\n"
    return context

# -------------------------------------------------------------
# STEP 5: LLM Answer Generation (Reference: 3. llm call.py & retreive.py)
# -------------------------------------------------------------
def generate_answer(question, context):
    """Generates an answer using LLM based strictly on provided context."""
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

    prompt = f"""
You are a helpful Q&A assistant. Answer the question ONLY using the context below.
If the answer cannot be found in the context, reply "I do not have information about this in my database."

Context:
{context}

Question:
{question}

Answer:
"""
    response = llm.invoke(prompt)
    return response.content

# Simple script runner to ingest sample docs
if __name__ == "__main__":
    print("=== Running RAG Pipeline Ingestion ===")
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)
        vectorstore = create_vectorstore(chunks)
        print("RAG Ingestion Complete!\n")

    user = input("Enter Question: ")
    context = retrieve_context(user, vectorstore)
    print("Context:", context)
    answer = generate_answer(user, context)
    print("Answer: ", answer)
