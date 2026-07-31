from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings 
from langchain_chroma import Chroma 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
import os 
import warnings 
from langchain_huggingface import HuggingFaceEmbeddings
warnings.filterwarnings(action='ignore')

direct = 'db/chroma_db'
if not os.path.exists(direct):
    os.makedirs(direct)
    
doc_path="docs"
def load_documents(doc_path):
    if not os.path.exists(doc_path):
        raise FileNotFoundError("Directory not found")
    # text directory loader 
    textloader= DirectoryLoader(doc_path, glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding":"utf-8"})
    documents= textloader.load()
    # pdf directory loader
    # pdfloader= DirectoryLoader(doc_path, glob="*.pdf", loader_cls=PyPDFLoader)
    # pdf_data= pdfloader.load()
    
    # documents.append(pdf_data)
    if len(documents)==0:
        raise FileNotFoundError("Directory is empty")
    
    return documents 

def chunk_documents(documents):
    splitter= RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks= splitter.split_documents(documents)
    
    if len(chunks)==0:
        raise ValueError('No chunks created')
    print("length of chunks",len(chunks))
    
    return chunks


def create_vector(chunks,directory):
    print("------create vector on give path----")
    embedder = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )
    vector = Chroma.from_documents(chunks, embedding=embedder, persist_directory=directory)
    print("Vector created successfully")
    return vector 
    
if __name__=="__main__":
    docs= load_documents(doc_path=doc_path)
    chunks= chunk_documents(docs)
    vector= create_vector(chunks, directory=direct)
    

    
    
    
    