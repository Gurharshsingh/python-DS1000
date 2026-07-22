import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")


query = input("Enter your query: ")

# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "openrouter/free",
    "messages": [
        {
          "role": "user",
          "content": query
        }
      ],
    "reasoning": {"enabled": True}
  })
)

# Extract the assistant message with reasoning_details
response = response.json()


# print(response)
# response = response['choices'][0]['message']
print(response)

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": query},
  {
    "role": "assistant",
    "content": response.get('content'),
    "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
  },
  {"role": "user", "content": "Give a proper structure to learn langchain."}
]

# Second API call - model continues reasoning from where it left off
response2 = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "openrouter/free",
    "messages": messages,  # Includes preserved reasoning_details
    "reasoning": {"enabled": True}
  })
)


response2 = response2.json()
response2 = response2['choices'][0]['message']['content']
print(response2)


