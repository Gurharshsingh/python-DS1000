import os
import requests
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("OPEN_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# 1. Zero-Shot Prompting (Direct question with no examples)
# print("--- 1. Zero-Shot Prompting ---")
# zero_shot_prompt = "Classify the sentiment of this review as Positive or Negative: 'The battery dies in 2 hours, totally useless!'"

# data = {
#     "model": "openrouter/free",
#     "messages": [{"role": "user", "content": zero_shot_prompt}]
# }

# response = requests.post(API_URL, headers=headers, json=data).json()
# print("Prompt:", zero_shot_prompt)
# print("Answer:", response['choices'][0]['message']['content'].strip())


# 2. Few-Shot Prompting (Providing examples to guide the output format/style)
# print("\n--- 2. Few-Shot Prompting ---")
# few_shot_prompt = """Classify reviews like the examples below:

# Review: 'I love the high-quality screen.' -> Product: Screen | Sentiment: Positive
# Review: 'The buttons are hard to press.' -> Product: Buttons | Sentiment: Negative
# Review: 'The case scratches too easily.' -> """

# data = {
#     "model": "openrouter/free",
#     "messages": [{"role": "user", "content": few_shot_prompt}]
# }

# response = requests.post(API_URL, headers=headers, json=data).json()
# print("Prompt:\n", few_shot_prompt)
# print("Answer:", response['choices'][0]['message']['content'].strip())


# 3. Prompt-Based Persona Control (System instructions to control LLM behavior)
print("\n--- 3. Controlling LLM Behavior via System Prompts ---")
system_persona = "You are a Shakespearean actor. Respond in dramatic, poetic Old English."
user_question = "What is Python?"

data = {
    "model": "openrouter/free",
    "messages": [
        {"role": "system", "content": system_persona},
        {"role": "user", "content": user_question}
    ]
}

response = requests.post(API_URL, headers=headers, json=data).json()
print(f"System Persona: {system_persona}")
print(f"Question: {user_question}")
print("Response:", response['choices'][0]['message']['content'].strip())
