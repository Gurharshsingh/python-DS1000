import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load variables from the .env file into the environment
load_dotenv()

def explore_inference_api():
    print("--- Exploring Inference APIs ---")
    print("The Inference API lets you run models on Hugging Face's servers without downloading them.")
    print("This requires virtually no local memory and is very fast.\n")
    
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("NOTE: No 'HF_TOKEN' environment variable found.")
        print("To use the Inference API in production, you need a free token from https://huggingface.co/settings/tokens")
        print("We will attempt an unauthenticated request, but it may fail or be rate-limited.\n")
    
    # Initialize the client (it uses HF_TOKEN from environment automatically if available)
    # We use a popular sentiment analysis model that is currently supported by the free API
    client = InferenceClient("cardiffnlp/twitter-roberta-base-sentiment-latest", token=hf_token)
    
    print(f"Sending request to the Cloud API using the official Hugging Face library...")
    try:
        # Task: text classification
        response = client.text_classification("i am neither happy nor sad")
        print("\n--- API Response (Properly Formatted) ---")
        # print(response)
        for result in response:
            print(f"Label: {result.label.upper()} | Confidence: {result.score:.2%}")
    except Exception as e:
        print(f"\nAPI request failed: {e}")
    print("\n")

if __name__ == "__main__":
    print("=== Welcome to the Hugging Face Ecosystem ===\n")
    explore_inference_api()




#i played cricket today i am very happy  - 90% positive
# i got less marks , i am sad - 80%- negative