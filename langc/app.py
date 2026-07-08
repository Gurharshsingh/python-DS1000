from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_classic.chains import LLMChain, SequentialChain
import streamlit as st

'''
--- ORIGINAL CODE COMMENTED OUT ---
# st.congfig(title = "Ollama")

llm = ChatOllama(model="tinyllama:latest", temperature=0.5)

# output_parser = StrOutputParser()

prompt = PromptTemplate(
    input_variables = ["subject"],
    template = "Write a poem about {subject}"
)

#chain definition

chain = prompt | llm  #output_parser

user  = input("Enter subject: ")
print(chain.invoke({"subject": user}))

# LLMchain
# Sequentialchain
-----------------------------------
'''

# Streamlit App Configuration
st.set_page_config(page_title="LangChain Blog Generator", page_icon="📝")
st.title("📝 AI Blog Generator")
st.write("Generate a full blog post from a single topic using Sequential Chains!")

# User input for the topic
topic = st.text_input("Enter a blog topic:", placeholder="e.g., Artificial Intelligence in Healthcare")

# Button to trigger generation
if st.button("Generate Blog"):
    if topic:
        with st.spinner("Generating your blog step-by-step..."):
            try:
# Initialize the LLM
llm = ChatOllama(model="tinyllama:latest", temperature=0.7)

# 1. Chain to create a blog title
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Create a catchy and engaging blog title about this topic: {topic}"
)
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key="title")

# 2. Chain to create an outline based on the title
outline_prompt = PromptTemplate(
    input_variables=["title"],
    template="Create a structured outline for a blog post titled '{title}'. Make it concise."
)
outline_chain = LLMChain(llm=llm, prompt=outline_prompt, output_key="outline")

# 3. Chain to write the blog post based on the title and outline
blog_prompt = PromptTemplate(
    input_variables=["title", "outline"],
    template="Write a comprehensive blog post titled '{title}' using the following outline:\n\n{outline}\n\nBlog Content:"
)
blog_chain = LLMChain(llm=llm, prompt=blog_prompt, output_key="blog_content")

# Combine them using a SequentialChain
overall_chain = SequentialChain(
    chains=[title_chain, outline_chain, blog_chain],
    input_variables=["topic"],
    output_variables=["title", "outline", "blog_content"],
    verbose=True
)

topic = input("Enter a blog topic: ")
print("\nGenerating blog...\n")

# Run the sequential chain
result = overall_chain.invoke({"topic": topic})

print("==== TITLE ====")
print(result["title"])
print("\n==== OUTLINE ====")
print(result["outline"])
print("\n==== BLOG POST ====")
print(result["blog_content"])
