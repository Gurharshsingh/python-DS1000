import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env
load_dotenv()

client = InferenceClient(
    provider="fal-ai",
    api_key=os.getenv("HF_TOKEN"),
)

# Call the image generation API (returns a PIL Image object)
image = client.text_to_image(
    prompt="A futuristic cyberpunk city skyline at sunset, highly detailed, 8k resolution",
    model="black-forest-labs/FLUX.1-dev" # You can swap this for other text-to-image models
)

# Save the generated image
image.save("cyberpunk_city.png")
print("Image saved successfully as cyberpunk_city.png!")

