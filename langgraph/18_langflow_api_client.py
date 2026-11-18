"""
LangFlow API Client Demo
========================
Shows how to query an exported LangFlow visual pipeline from Python.

Prerequisites:
  1. Start LangFlow in your terminal: python -m langflow run
  2. Click 'API' in LangFlow top-right corner to get your Flow ID.
"""

import requests

# 1. LangFlow Local Server Endpoint
FLOW_ID = "my-first-flow"  # Replace with your Flow ID from LangFlow
API_URL = f"http://127.0.0.1:7860/api/v1/run/{FLOW_ID}"

# 2. Prepare the Query
user_question = "What is the capital of France and what is 25 * 40?"
payload = {
    "input_value": user_question,
    "input_type": "chat",
    "output_type": "chat",
    "tweaks": {}  # Optional: override temperature, model, or prompt at runtime
}

# 3. Call the LangFlow Visual Agent via REST API
def query_langflow():
    print(f"Sending Question to LangFlow: '{user_question}'...")
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Extract response text from standard LangFlow output payload
            output_text = result["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            print("\n--- Response from LangFlow Visual Agent ---")
            print(output_text)
        else:
            print(f"Server returned status {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n[!] Could not connect to LangFlow.")
        print("Make sure LangFlow is running in another terminal window:")
        print("  -> Run: python -m langflow run")

if __name__ == "__main__":
    query_langflow()

