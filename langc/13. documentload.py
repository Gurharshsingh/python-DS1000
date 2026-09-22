from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, DirectoryLoader




# loader  = TextLoader("docs/name.txt")
# loader  = PyPDFLoader("docs/new.pdf")   
# loader = CSVLoader("docs/cars.csv")
loader  = DirectoryLoader("docs", glob = "*.txt",loader_cls=TextLoader)




docs = loader.load()
print(len(docs))

for i,j in enumerate(docs):
    print(f"Document{i+1}, metadata: {j.metadata}")
    print(f"page content: {j.page_content}")





















# csvloader

# csv = CSVLoader("docs/cars.csv")
# csv_doc = csv.load()
# # print(csv_doc)
# print(len(csv_doc))


# # #directory loader

# dloader = DirectoryLoader("docs", glob = "*.txt",loader_cls=TextLoader, loader_kwargs={'encoding' : 'utf-8'})
# documents = dloader.load()
# print(len(documents))


# for i in documents:
#     print(i.metadata['source'])
#     print(i.page_content)







#document load -> text -> text split -> chunks - embedding -> ingestion -> vector store 







