from langchain_community.chat_models import ChatOpenAI
import requests
import os 
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")
api_key1 = os.getenv("OPEN_API_KEY")


@tool
def get_weather(city:str)->str:

    """Get the current weather of the city"""

    try:
        base_url = "https://api.weatherapi.com/v1/current.json"
        params = {"key":api_key,"q":city}

        response = requests.get(base_url,params)
        data  = response.json()
    
        return data

    except Exception as e:
        return f"error: {e}"


@tool
def currency_convert(amount:float,from_currency:str,to_currency:str) -> str:
    """convert currency from one currency to another currency"""

    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        response = requests.get(url)

        data = response.json()

        rate = data['rates'][to_currency.upper()]
        converted = amount * rate

        return(f"{amount}{from_currency.upper()} = {converted}{to_currency.upper()}")
    except Exception as e:
        return f"error: {e}"


tools = [get_weather,currency_convert]

llm = ChatOllama(model = "llama3.2:latest",temperature=0.5)

# llm = ChatOpenAI(
#     model_name="openrouter/free",
#     openai_api_key=api_key1,
#     openai_api_base="https://openrouter.ai/api/v1",
#     temperature=0.5
# )


llm1 = llm.bind_tools(tools)

def create_tool_bot(query):

    messages = [HumanMessage(content = query)]

    response = llm1.invoke(messages)

    if response.tool_calls:

        tool_call = response.tool_calls[0]
        tool_name = tool_call['name']
        tool_args = tool_call['args']

        print(f"Selected tool: {tool_name}")
        print(f"Arguments: {tool_args}")

        selected_tool = next(tool for tool in tools if tool.name == tool_name)

        result = selected_tool.invoke(tool_args)

        print("Result: ",result)

        messages.append(response)
        messages.append(HumanMessage(content = str(result)))

        final_response = llm.invoke(messages)
        return final_response.content

    else:
        return response.content



while True:
    user = input("User: ")
    result = create_tool_bot(user)
    print("Agent: ",result)