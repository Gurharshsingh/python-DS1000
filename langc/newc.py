from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama



llm = ChatOllama(model="phi3:mini",temperature=0.5)

output_parser=StrOutputParser()
prompt = PromptTemplate(
    input_variables=["subject"],
    template="Write a short poem about {subject}"
)

#chain definition using langchain expression language
# chain=prompt | llm | output_parser


# user=st.text_input("Enter your subject of the poem: ")

# result=chain.invoke({'subject':user})
# st.write(result)



# 1. LLMChain
from langchain_classic.chains import LLMChain,SequentialChain
# chain2=LLMChain(
#     llm=llm,
#     prompt=prompt,
#     output_key="poem"
# )

# user=input("Enter your subject: ")

# result=chain2.invoke(user)
# print(result)



prompt1=PromptTemplate(input_variables=['Subject'],template="""
    Title:
    You are the best title generator generate the tilte on the {Subject}
    given by the user for by blog
    Title
""")

prompt2=PromptTemplate(input_variables=['Title'],template="""
    Outline:
    You are the best outliner generate the outline on the {Title}
    given by the user for by blog
    Outline
""")


prompt3=PromptTemplate(input_varibles=['Outline'],template="""
    Blog:
    You are the best content writer generate the blog on the {Outline}
    given by the user for by blog
    Blog
""")


title_chain=LLMChain(llm=llm,prompt=prompt1,output_key="Title")

outline_chain=LLMChain(llm=llm,prompt=prompt2,output_key="Outline")

blog_chain=LLMChain(llm=llm,prompt=prompt3,output_key="Blog")

# 2. Sequential Chain
# final_chain=SequentialChain(chains=[title_chain,outline_chain,blog_chain],input_variables=['Subject'],output_variables=['Title','Outline','Blog'],verbose=True)


# user =input("Enter your subject for the blog: ")

# result=final_chain.invoke({'Subject':user})
# print(result['Title'])
# print(result['Outline'])
# print(result['Blog'])


# Simple Sequential Chain
from langchain_classic.chains import SimpleSequentialChain

final_chain=SimpleSequentialChain(chains=[title_chain,outline_chain,blog_chain])

result=final_chain.invoke("Artificial Intelligence")

print(result)


