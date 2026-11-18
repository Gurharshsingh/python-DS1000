import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# Initialize Hugging Face Inference Client
client = InferenceClient(
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    token=os.getenv("HF_TOKEN")
)

# Perform sentiment analysis
text = "I scored good marks i am going to party"
response = client.text_classification(text)

# Print results
for result in response:
    print(f"Label: {result.label.upper()} | Confidence: {result.score:.2%}")