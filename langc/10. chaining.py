import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_classic.chains import LLMChain, SequentialChain, SimpleSequentialChain
import streamlit as st


st.set_page_config(page_title="Blog generator")
st.title("Blog Generator through Chaining")

st.sidebar.title('Blogs')




# 1. Load the OpenRouter API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# # 2. Initialize the OpenRouter LLM
llm = ChatOpenAI(
    model_name="openrouter/free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.5
)

# llm = ChatOllama(model="phi3:mini",temperature=0.5)

output_parser = StrOutputParser()


# prompt = PromptTemplate(input_variables=['Subject'],
#                         template="Write a poem about {subject}")

# # Langchain Expression language(LCEL)

# chain = prompt | llm | output_parser


# user = input("enter subject of the poem: ")

# result = chain.invoke(user)

# print(result)


#LLM Chain

# chain1 = LLMChain(llm=llm,prompt=prompt,output_parser = output_parser ,output_key="poem")

# user = input("Enter subject: ")

# result = chain1.invoke(user)
# print(result)


# blog - title -> outine -> body - result-> 



prompt1 = PromptTemplate(input_variables=['subject'],
                        template = """
                        Title: 
                        you are an excellent title generator generate 
                        one title for the blog on {subject}
                        Title
                        """)

prompt2 = PromptTemplate(input_variables=['Title'],
                        template = """
                        Outline: 
                        you are an excellent outline generator generate 
                        one outline for the blog on {subject}
                        Outline
                        """)

prompt3 = PromptTemplate(input_variables=['Outline'],
                        template = """
                        Blog: 
                        you are an excellent blog generator generate 
                         blog on the {subject}
                        Blog
                        """,)



title_chain = LLMChain(llm=llm, prompt= prompt1, output_key= 'Title')

outline_chain = LLMChain(llm=llm, prompt= prompt2, output_key= 'Outline')

blog_chain = LLMChain(llm=llm, prompt= prompt3, output_key= 'Blog')


final_chain = SequentialChain(chains=[title_chain,outline_chain,blog_chain],input_variables=['subject'],output_variables=['Title','Outline','Blog'])


# final_chain = SimpleSequentialChain(chains=[title_chain,outline_chain,blog_chain])
subject = st.sidebar.text_input("Enter subject:")

result = final_chain.invoke(subject)
st.write(result)

# st.write(result['output'])
# print('Title: ',result['Title'])
# print('Outline:',result['Outline'])
# print("Blog:" ,result['Blog'])



















