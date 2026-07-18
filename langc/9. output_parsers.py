import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# 1. Load the OpenRouter API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Initialize the OpenRouter LLM
llm = ChatOpenAI(
    model_name="openrouter/free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0
)

# ---------------------------------------------------------------------------
# 1. StrOutputParser Demo
# ---------------------------------------------------------------------------
print("=== 1. StrOutputParser Demo ===")
str_parser = StrOutputParser()

# Format prompt manually
prompt_template = PromptTemplate.from_template("What is {topic}?, answer in plain string no formatiing showing \n and evrything")
formatted_prompt = prompt_template.format(topic="Machine Learning")
print("Formatted Prompt:")
print(formatted_prompt)

# Invoke LLM
response = llm.invoke(formatted_prompt)
print("\nRaw LLM Response Object (AIMessage):")
print(repr(response))

# Parse output manually
parsed_string = str_parser.invoke(response)
print("\nParsed Result (Plain String):")
print(parsed_string)


# ---------------------------------------------------------------------------
# 2. JsonOutputParser 
# ---------------------------------------------------------------------------
print("\n=== 2. JsonOutputParser ===")
json_parser = JsonOutputParser()

# Plain query string asking for JSON format
query = "Explain Deep Learning in JSON format with keys: topic, definition, advantages."
print("Query:")
print(query)

# # Invoke LLM
response = llm.invoke(query)
print("\nRaw LLM Response String:")
print(response.content)

# # Parse JSON manually
parsed_dict = json_parser.parse(response.content)
print("\nParsed Result (Dictionary):")
print(parsed_dict)
print("Type:", type(parsed_dict))




