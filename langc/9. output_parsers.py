from langchain_core.prompts import message
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama

# 1. Load the OpenRouter API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Initialize the OpenRouter LLM
llm = ChatOpenAI(
    model_name="openrouter/free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7
)


# llm1 = ChatOllama(model="tinyllama:latest",
#                 temperature=0.7)

# s_parser = StrOutputParser()


# template = PromptTemplate.from_template("what is {topic}, ")
# formatted_message = template.format(topic = "LLM")


# response = llm.invoke(formatted_message)
# print(response)


# result = s_parser.invoke(response)
# print(result)


j_parser = JsonOutputParser()

temp = ChatPromptTemplate.from_messages([('system', 'you are an expert in  {subject} keep your tone {tone}'),
                                         ('human', "explain {topic} and answer in properly sturctured json format like topic, definition etc")])

f_message  = temp.format(subject = "History", tone = "Funny", topic = "Roman Empire")

response = llm.invoke(f_message)
print(response.content)

print("\n\n\n\n")

result1 = j_parser.parse(response.content)
print(result1)







# ---------------------------------------------------------------------------
# # 2. JsonOutputParser 
# # ---------------------------------------------------------------------------
# print("\n=== 2. JsonOutputParser ===")
# json_parser = JsonOutputParser()

# # Plain query string asking for JSON format
# query = "Explain Deep Learning in JSON format with keys: topic, definition, advantages."
# print("Query:")
# print(query)

# # # Invoke LLM
# response = llm.invoke(query)
# print("\nRaw LLM Response String:")
# print(response.content)

# # # Parse JSON manually
# parsed_dict = json_parser.parse(response.content)
# print("\nParsed Result (Dictionary):")
# print(parsed_dict)
# print("Type:", type(parsed_dict))




