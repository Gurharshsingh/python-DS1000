from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

PERSIST_DIR = "db/chroma_db"


def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs = {"normalize_embeddings":True}
    )

    vectorstore = Chroma(       
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="my_documents"

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

    llm = ChatOllama(
        model = 'llama3.2:latest',
        temperature= 0.5
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
        print(chunks)


        context = build_context(chunks)

        answer = generate_answer(question, context)

        print("\n FINAL ANSWER")
        print("="*70)
        print(answer)





# supervised - classification , regressions
#unsupervised - clustering  , dbscan , kmeans clustering 