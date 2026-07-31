from langchain_text_splitters import RecursiveCharacterTextSplitter


data=["Even though it started pouring rain right in the middle of our afternoon picnic, we quickly packed up all our food and decided to finish our lunch inside the cozy little coffee shop down the street",
"Because she wanted to make sure she was fully prepared for the upcoming job interview, she spent the entire weekend researching the company's history and practicing her answers to potential questions.",
"When we finally arrived at the bustling international airport after a long and exhausting drive, we realized we had accidentally left our passports sitting on the kitchen table back at the house.",
"Although the new Italian restaurant in the downtown district is a bit more expensive than the local diners, the incredible flavor of their handmade pasta is absolutely worth every single penny.",
"After the marathon race ended, the exhausted runners were grateful to receive medals, water bottles, and refreshing snacks at the finish line."]



splitter  = RecursiveCharacterTextSplitter(chunk_size =50,chunk_overlap = 20)

chunks=[]

for i in data:
    l = splitter.split_text(i)
    chunks.extend(l)

print(chunks)

for chunk in chunks:
    print("*"*20)
    print(chunk)

print("length of chunks",len(chunks))



from langchain_huggingface import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

vectors = embedder.embed_documents(chunks)

for i,vector in enumerate(vectors):
    print("Vector",i+1)
    print(f"Dimension of vector {len(vector)}")
    print(vector[:10])








































