import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
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