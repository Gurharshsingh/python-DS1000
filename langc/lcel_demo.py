from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough

print("🚀 LCEL Pipeline Demo")
topic = input("Enter a blog topic (e.g., Space Exploration): ")

print("\nChoose your Pipeline Type:")
print("1. With .assign() (Clean & Automatic)")
print("2. Without .assign() (Manual Dictionary Mapping)")
choice = input("Enter 1 or 2: ")

# Initialize the LLM
llm = ChatOllama(model="tinyllama:latest", temperature=0.7)

# Define the components (Chains)
title_chain = PromptTemplate.from_template("Create a short, catchy blog title about: {topic}") | llm | StrOutputParser()
outline_chain = PromptTemplate.from_template("Create a 3-point outline for a blog post titled '{title}'.") | llm | StrOutputParser()
blog_chain = PromptTemplate.from_template("Write a very short blog post titled '{title}' using this outline:\n{outline}\n\nBlog:") | llm | StrOutputParser()

if choice == "1":
    print("\nUsing RunnablePassthrough.assign() - The automatic way!")
    pipeline = (
        {"topic": RunnablePassthrough()}
        | RunnablePassthrough.assign(title=title_chain)
        | RunnablePassthrough.assign(outline=outline_chain)
        | RunnablePassthrough.assign(blog_content=blog_chain)
    )
else:
    print("\nUsing Manual Dictionary Mapping - Exactly what .assign() does under the hood!")
    pipeline = (
        {"topic": RunnablePassthrough()}
        | {
            "topic": lambda x: x["topic"],
            "title": title_chain
        }
        | {
            "topic": lambda x: x["topic"],
            "title": lambda x: x["title"],
            "outline": outline_chain
        }
        | {
            "topic": lambda x: x["topic"],
            "title": lambda x: x["title"],
            "outline": lambda x: x["outline"],
            "blog_content": blog_chain
        }
    )

print("\nGenerating your blog step-by-step...\n")
result = pipeline.invoke(topic)

# Display Results
print("==== TITLE ====")
print(result["title"])

print("\n==== OUTLINE ====")
print(result["outline"])

print("\n==== BLOG POST ====")
print(result["blog_content"])
