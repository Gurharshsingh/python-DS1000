import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY= os.getenv('API_KEY')


query = input("Enter the topic you want to read: ")


url = f"https://newsapi.org/v2/everything?q={query}&from=2026-07-10&sortBy=publishedAt&apiKey={API_KEY}"

response = requests.get(url)

result = response.json()
# print(result)


# print(result['articles'][0]['title'])
# print(result['articles'][0]['description'])


for i in range(10):
    print(result['articles'][i]['title'])
    print()
    print(result['articles'][i]['description'])
    print("\n\n")