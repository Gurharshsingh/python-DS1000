import requests
import json
from dotenv import load_dotenv  # python-dotenv pip install python-dotenv
import os   
import sys

# # Configure stdout to handle Unicode on Windows consoles without crashing
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
API_KEY=os.getenv('OPEN_API_KEY')

# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "openrouter/free",  # Use openrouter/free to avoid 429 rate limit errors
    "messages": [
        {
          "role": "user",
          "content": "Whats an LLM?"
        }
      ],
    "reasoning": {"enabled": True}
  })
)

# Extract the assistant message with reasoning_details
response = response.json()
response = response['choices'][0]['message']

# Print the first response content
print("First response:")
print(response.get('content'))
print()

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "Can i create my own LLM?"},
  {
    "role": "assistant",
    "content": response.get('content'),
    "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# Second API call - model continues reasoning from where it left off
# Re-added the authorization headers here so the request does not fail
response2 = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "openrouter/free",  # Use openrouter/free to avoid 429 rate limit errors
    "messages": messages,  # Includes preserved reasoning_details
    "reasoning": {"enabled": True}
  })
)

# Print the final output response
print("Second response:")
print(response2.json()['choices'][0]['message']['content'])