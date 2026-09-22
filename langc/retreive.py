from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

PERSIST_DIR = "db/chroma_db"


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs = {"normalize_embeddings":True}
    )

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    return vectorstore



def retrieve_chunks(query, k=5):
    vectorstore  = load_vectorstore()
    results  = vectorstore.similarity_search(query= query, k = k)

    return results


def build_context(chunks):

    context = ""

    for i, chunk in enumerate(chunks, start= 1):
        context += f"\n\n-----Chunk{i}-----\n"
        context += chunk.page_content

    return context


def generate_answer(question, context):

    api_key = os.getenv("OPEN_API_KEY")
    if api_key:
        print("Using OpenRouter for generation...")
        llm = ChatOpenAI(
            model_name="openrouter/free",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.5
        )
    else:
        print("Using local Ollama for generation...")
        llm = ChatOllama(
            model='llama3.2:latest',
            temperature=0.5
        )


    prompt = f"""

    You are a helpful assistant.


    Answer ONLY using the provided context

    context= {context}

    question = {question}


    Answer:


    Strict Rules:

    1. Do not answer any question out of context

    2. If you dont have any answer just reply i dont have context about this question

    """

    response = llm.invoke(prompt)
    return response.content


if __name__  == "__main__":

    while True:
        question = input("Ask Your question")

        if question.lower() == "exit":
            break

        print("\n retrieving chunks....")

        chunks = retrieve_chunks(question)


        context = build_context(chunks)
        # print(context)

        answer = generate_answer(question, context)

        print("\n FINAL ANSWER")
        print("="*70)
        print(answer)
    

    



















































































































# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_ollama import ChatOllama

# PERSIST_DIR = "db/chroma_db"


# def load_vectorstore():

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2",
#         encode_kwargs={"normalize_embeddings": True}
#     )

#     vectorstore = Chroma(
#         persist_directory=PERSIST_DIR,
#         embedding_function=embeddings
#     )

#     return vectorstore


# def retrieve_chunks(query, k=5):

#     vectorstore = load_vectorstore()

#     results = vectorstore.similarity_search(
#         query=query,
#         k=k
#     )

#     return results


# def build_context(chunks):

#     context = ""

#     for i, chunk in enumerate(chunks, start=1):

#         context += f"\n\n----- Chunk {i} -----\n"
#         context += chunk.page_content

#     return context


# def generate_answer(question, context):

#     llm = ChatOllama(
#         model="llama3.2:latest",
#         temperature=0.5
#     )

#     prompt = f"""
# You are a helpful AI assistant.

# Answer ONLY using the provided context.

# Context:
# {context}

# Question:
# {question}

# Answer:


# STRICT RULES:
# 1. Do not answer any question out of the context.
# 2. If you don't know the answer just reply i donot have any context about the question you have asked
# """

#     response = llm.invoke(prompt)

#     return response.content


# if __name__ == "__main__":

#     while True:
#         question = input("Ask Question: ")

#         if question.lower() == "exit":
#             break

#         print("\nRetrieving chunks...\n")

#         chunks = retrieve_chunks(question)

#         # print("=" * 70)
#         # print("RETRIEVED CHUNKS")
#         # print("=" * 70)

#         # for i, chunk in enumerate(chunks, start=1):

#     #       print(f"\nChunk {i}")
#     #       print("-" * 50)

#     #       print(chunk.page_content[:800])

#     #       print("\nMetadata:")
#     #       print(chunk.metadata)

#         context = build_context(chunks)

#         # print("\n")
#         # print("=" * 70)
#         # print("CONTEXT SENT TO LLM")
#         # print("=" * 70)

#         # print(context[:3000])

#         answer = generate_answer(
#             question=question,
#             context=context
#         )

#         # print("\n")
#         # print("=" * 70)
#         # print("FINAL ANSWER")
#         # print("=" * 70)

#         print(answer)