import os
from  dotenv import load_dotenv
import requests
load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)
query = input("Enter query")
url =f"https://newsapi.org/v2/everything?q={query}&from=2026-09-01&sortBy=publishedAt&apiKey={API_KEY}"
result=requests.get(url)
print(result)
data=result.json()
print(data)