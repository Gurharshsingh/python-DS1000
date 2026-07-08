import requests
from dotenv import load_dotenv  # python-dotenv pip install python-dotenv
import os   

load_dotenv()
API_KEY=os.getenv('API_KEY')

# url=f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
# result=requests.get(url)
# # print(result.json())

# result = result.json()

# # print(result['articles'][0]['author'])
# # print(result['articles'][0]['title'])
# # print(result['articles'][0]['description'])
# # print(result['articles'][0]['url'])
# # print(result['articles'][0]['urlToImage'])
# # print(result['articles'][0]['publishedAt'])
# # print(result['articles'][0]['content'])

# for i in range(10):
#     print(f"Healdine {i}")
#     print(result['articles'][i]['title'])
#     print(result['articles'][i]['description'])
#     print()

query=input("Enter your query :")
url=f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"

result=requests.get(url)

result=result.json()

print(result)