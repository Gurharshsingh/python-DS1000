import os
from rag_pipeline import (
    load_documents,
    split_documents,
    create_vectorstore,
    load_vectorstore,
    retrieve_context,
    generate_answer,
    DB_DIR
)
import streamlit as st

st.set_page_config(page_title="RAG Q&A Assistant", page_icon="🐻")

st.title("🐻 RAG Q&A Assistant")


def run_qa_assistant():
    """Simple Interactive Q&A Assistant."""
    print("=" * 60)
    print("           WELCOME TO THE SIMPLE RAG Q&A ASSISTANT          ")
    print("=" * 60)

    # Step 1: Ensure VectorStore is initialized
    if not os.path.exists(DB_DIR):
        print("\n[DB] Vector database not found. Ingesting documents...")
        docs = load_documents()
        if not docs:
            print("[Error] No documents found to ingest. Please place text files in 'sample_docs' folder.")
            return
        chunks = split_documents(docs)
        vectorstore = create_vectorstore(chunks)
    else:
        print("\n[DB] Loading existing vector database...")
        vectorstore = load_vectorstore()

    print("[DB] Ready! Ask any question based on your documents.")
    print("Type 'exit' or 'quit' to end the session.\n")

    # Step 2: Interactive loop
    i = 0 
    # while True:
    try:
        user_question = st.text_input("\nAsk Question > ").strip()
        
            

        if user_question.lower() in ["exit", "quit"]:
            st.write("Goodbye!")
            

        st.write("-> Searching relevant document chunks...")
        context = retrieve_context(user_question, vectorstore, k=3)

        st.write("-> Generating answer from LLM...")
        answer = generate_answer(user_question, context)

        st.write("\n" + "=" * 60)
        st.write("ANSWER:")
        st.write("=" * 60)
        st.write(answer)
        st.write("=" * 60)
            


    except KeyboardInterrupt:
        st.write("\nGoodbye!")
    except Exception as e:
        st.write(f"[Error] An error occurred: {e}")
    i+=1

if __name__ == "__main__":
    run_qa_assistant()
