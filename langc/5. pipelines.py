from transformers import pipeline

# ==========================================
# 1. Text Generation Pipeline
# ==========================================
# print("--- Running Text Generation ---")
# generator = pipeline("text-generation", model="gpt2")

# # Customizing generation parameters:
# res_gen = generator(
#     "Artificial intelligence is", 
#     max_length=40,               # Maximum length of the generated output (includes prompt)
#     num_return_sequences=2,      # Generate multiple different text variations
#     do_sample=True,              # Enable sampling (adds variation, default is False/greedy search)
#     temperature=0.8             # Controls creativity (higher = more creative/random, lower = more focused)
# )
# print(res_gen)





# ==========================================
# 2. Classification Pipeline (Sentiment Analysis)
# ==========================================
print("--- Running Classification ---")
classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
res_class = classifier(
    "I absolutely love learning about NLP!",
    top_k=None                 # Set to None to return probability scores for ALL classes (Positive AND Negative) instead of just the top one
)
print(res_class)
