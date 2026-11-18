import os
import tempfile


from pypdf import PdfReader

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama


import streamlit as st
st.subheader("MY FIRST PROJECT")
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="🎠"
    
)

st.title(" PDF Question Answering Chatbot")

st.write(
    "Upload your PDF and ask questions. "
    "The chatbot will answer using your document."
)



if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "topics" not in st.session_state:
    st.session_state.topics = []

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None




def detect_topic(question):

    q = question.lower()

    if "list" in q:
        topic = "Python List"

    elif "tuple" in q:
        topic = "Python Tuple"

    elif "dictionary" in q or "dict" in q:
        topic = "Python Dictionary"

    elif "function" in q:
        topic = "Python Functions"

    elif "loop" in q:
        topic = "Python Loops"

    elif "class" in q or "object" in q:
        topic = "Python OOP"

    elif "python" in q:
        topic = "Python Basics"

    elif "rag" in q:
        topic = "RAG"

    else:
        topic = "General Questions"

    print(f"[VERBOSE - TOPIC] Detected topic: '{topic}' for question: '{question}'")
    return topic



with st.sidebar:

    st.header(" Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

    build_button = uploaded_file is not None
        
    

    st.caption("AI Model: qwen2.5:3b")

    st.divider()

    
    st.header("Memory & Topics")

    st.write("Topics")

    if st.session_state.topics:

        for topic in st.session_state.topics:
            st.write( topic)

    else:
        st.caption("No topics yet.")

    st.divider()

    
    st.write("Chat History")

    if st.session_state.messages:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.write( message["content"])

    else:
        st.caption("No questions asked yet.")

    st.divider()

    
    if st.button(" Clear Memory", use_container_width=True):

        print("[VERBOSE - MEMORY] 'Clear Memory' button pressed. Resetting chat messages and topics.")
        st.session_state.messages = []
        st.session_state.topics = []

        st.rerun()



if build_button:

    if uploaded_file is None:

        st.warning(" upload  PDF first.")

    else:

        temp_path = None

        try:

            with st.spinner(""):

                print(f"\n[VERBOSE - PDF UPLOAD] Received file: '{uploaded_file.name}' ({uploaded_file.size} bytes)")
                
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_path = temp_file.name

                print(f"[VERBOSE - TEMP FILE] Saved temporary PDF to: {temp_path}")
                
                reader = PdfReader(temp_path)

                if len(reader.pages) == 0:

                    raise ValueError(
                        "PDF has no pages."
                    )

                print(f"[VERBOSE - PDF READER] Found {len(reader.pages)} page(s) in document.")
                
                loader = PyPDFLoader(temp_path)

                documents = loader.load()

                print(f"[VERBOSE - LOADER] PyPDFLoader extracted {len(documents)} page document(s).")
                
                documents = [
                    doc for doc in documents
                    if doc.page_content.strip()
                ]

                if not documents:

                    raise ValueError(
                        "No readable text found in PDF. "
                        "Try a text-based PDF."
                    )

                print(f"[VERBOSE - FILTER] {len(documents)} non-empty readable pages retained.")
                
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1800,
                    chunk_overlap=100
                )

                chunks = splitter.split_documents(
                    documents
                )

                print(f"[VERBOSE - SPLITTER] Created {len(chunks)} text chunks (chunk_size=1800, overlap=100).")
                
                print("[VERBOSE - EMBEDDINGS] Loading HuggingFaceEmbeddings (all-MiniLM-L6-v2 on CPU)...")
                embeddings = HuggingFaceEmbeddings(
                    model_name=(
                        "sentence-transformers/"
                        "all-MiniLM-L6-v2"
                    ),
                    model_kwargs={
                        "device": "cpu"
                    }
                )

                print("[VERBOSE - VECTORSTORE] Building FAISS vector store in memory...")
                vectorstore = FAISS.from_documents(
                    chunks,
                    embeddings
                )

                print(f"[VERBOSE - VECTORSTORE] Successfully created FAISS index with {len(chunks)} chunks for '{uploaded_file.name}'.\n")
                
                st.session_state.vectorstore = vectorstore

                st.session_state.pdf_name = (
                    uploaded_file.name
                )

                
                st.session_state.messages = []
                st.session_state.topics = []

            st.success(
                # f"PDF processed successfully! "
                f"{len(chunks)} chunks created."
            )

        except Exception as e:

            print(f"[VERBOSE - ERROR] Error processing PDF: {e}")
            st.error(
                f"Error processing PDF: {e}"
            )

        finally:

            if temp_path and os.path.exists(temp_path):

                os.remove(temp_path)
                print(f"[VERBOSE - CLEANUP] Removed temporary file: {temp_path}")



for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if message.get("sources"):

            with st.expander(" View source pages"):

                for source in message["sources"]:

                    st.write(source)




question = st.chat_input(
    "Ask a question about your PDF"
)


if question:

    if st.session_state.vectorstore is None:

        st.warning(
            " upload  PDF first"
        )

    else:

        print("\n" + "=" * 65)
        print(f"[VERBOSE - USER INPUT] Question: '{question}'")
        
        topic = detect_topic(question)

    
        if topic not in st.session_state.topics:

            st.session_state.topics.append(
                topic
            )
            print(f"[VERBOSE - TOPICS] Added new topic to list: '{topic}'")

        
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        
        with st.chat_message("user"):

            st.markdown(question)

        try:

            with st.chat_message("assistant"):

                    print(f"[VERBOSE - SIMILARITY SEARCH] Querying FAISS vector store for top k=1 chunk...")
                    retrieved_docs = (
                        st.session_state.vectorstore
                        .similarity_search(
                            question,
                            k=1
                        )
                    )

                    print(f"[VERBOSE - RETRIEVAL] Found {len(retrieved_docs)} matching document chunk(s).")
                    
                    context_parts = []

                    sources = []

                    for doc in retrieved_docs:

                        page_number = (
                            doc.metadata.get(
                                "page", 0
                            ) + 1
                        )

                        context_parts.append(
                            f"[Page {page_number}]\n"
                            f"{doc.page_content}"
                        )

                        source = f"Page {page_number}"

                        if source not in sources:

                            sources.append(source)

                        preview = doc.page_content.strip()[:100].replace('\n', ' ')
                        print(f"  -> Source: Page {page_number} | Preview: \"{preview}...\"")

                    context = "\n\n".join(
                        context_parts
                    )

                  
                    messages = (
                        st.session_state.messages[:-1]
                    )

                    history_text = ""

                    for msg in messages:

                        history_text += (
                            f"{msg['role']}: "
                            f"{msg['content']}\n"
                        )

                    print(f"[VERBOSE - MEMORY] Loaded {len(messages)} previous message(s) from chat history.")

                    print("[VERBOSE - LLM INFERENCE] Initializing ChatOllama (model='qwen2.5:3b', temperature=0)...")
                    llm = ChatOllama(
                        model="qwen2.5:3b",
                        temperature=0
                    )

                   
                    prompt = f"""
You are a helpful PDF question-answering assistant.

Use the PDF context and conversation history.

Rules:
1. Answer using the PDF context.
2. If the answer is not in the PDF,
   say that you could not find it.
3. Do not invent information.
4. Remember the previous conversation.
5. Answer in the same language as the user.
6. Explain answers in simple language.

Previous conversation:
{history_text}

PDF context:
{context}

Current question:
{question}

Answer:
"""

                    print("[VERBOSE - LLM INFERENCE] Sending synthesized prompt to Ollama...")
                    response = llm.invoke(
                        prompt
                    )

                    answer = response.content
                    preview_ans = answer[:100].replace('\n', ' ')
                    print(f"[VERBOSE - LLM RESPONSE] Response generated ({len(answer)} chars): \"{preview_ans}...\"")

                
            st.markdown(answer)

                
            with st.expander(
                    " View source pages"
                ):

                    for source in sources:

                        st.write(source)

          
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            print(f"[VERBOSE - STATE] Assistant response and sources saved to session_state.")
            print("=" * 65 + "\n")

        except Exception as e:

            print(f"[VERBOSE - ERROR] Error generating answer: {e}")
            st.error(
                "Error generating answer. "
                "Check Ollama and your AI model. "
                f"Details: {e}"
            )
btn= st.button("Save")

if btn:
    print("[VERBOSE - UI] 'Save' button clicked.")
    st.success("Button clicked")
    st.snow()
