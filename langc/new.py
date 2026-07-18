#pip install langchain langchain-core langchain-ollama 
from langchain_ollama import ChatOllama 
from langchain_core.prompts import ChatPromptTemplate 
import streamlit as st
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
llm= ChatOllama(
    model='gemma3:1b',
)
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert AI Professor."),
#     ("human", "{question}")
# ])
# prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      """
#      You are an expert AI Professor.
#      Give answers in bullet points.
#      """),
#     ("human", "{question}")
# ])
prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
     Return the answer only in valid JSON.
     {{
         "topic":"",
         "definition":"",
         "Advantages":[]
     }}
     """),
    ("human", "{topic}")
])

# output_parser
# parser= StrOutputParser()  # output -> plain text
parser= JsonOutputParser()  # output -> In json format


# chain= prompt | llm # without output parser
chain= prompt | llm | parser 
st.header("langchain Ollama chat")

text= st.text_input('Enter Question here..')
if text:
    response= chain.invoke({
    'topic':{text}
    }) 
    st.write(response)
    # st.header(response['topic'])
    # st.subheader(response['definition'])
    # st.write(response['Advantages of Python'])
    
# ChatPromptTemplate.from_messages
# output parsers 
# stringoutputparser
# jsonoutputparser
# list.....