from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, DirectoryLoader



loader = TextLoader("langc/docs/name.txt")
doc = loader.load()
print(doc)
for i, j in enumerate(doc):
    print(f"Document{i+1}, metadata: {j.metadata}")
    print(f"page content: {j.page_content}")


#pdf loader 

# pdf = PyPDFLoader("langc/docs/new.pdf")
# pdf_doc = pdf.load()
# print(pdf_doc)


# for i, j in enumerate(pdf_doc):
#     print(f"Document{i+1}, metadata: {j.metadata}")
#     print(f"page content: {j.page_content}")


# csvloader

# csv = CSVLoader("langc/docs/cars.csv")
# csv_doc = csv.load()
# print(csv_doc)
# print(len(csv_doc))


# #directory loader

dloader = DirectoryLoader("langc/docs", glob = "*.txt",loader_cls=TextLoader, loader_kwargs={'encoding' : 'utf-8'})
documents = dloader.load()
print(len(documents))


for i in documents:
    print(i.metadata['source'])
    print(i.page_content)







#document load -> text -> text split -> chunks - embedding -> ingestion -> vector store 







