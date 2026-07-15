from langchain_huggingface import HuggingFaceEndpoint
# Initialize the model using Hugging Face's serverless Inference API
# Requires HUGGINGFACEHUB_API_TOKEN environment variable to be set
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b",
    huggingfacehub_api_token="key"
)
# Call the model
response = llm.invoke("how are you")
print(response)





