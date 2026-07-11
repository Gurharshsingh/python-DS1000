import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer <Open_API_KEY>",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "qwen/qwen3-next-80b-a3b-instruct:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })


)
print(response)

# print(response.json['choices'][0]['message']['content'])