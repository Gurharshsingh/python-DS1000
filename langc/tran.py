from transformers import pipeline #pip install transformers torch


# print("sentiment analysis.......")

# sentiment = pipeline("sentiment-analysis",model= "cardiffnlp/twitter-roberta-base-sentiment")

# user = input("Enter your sentence: ")


# result = sentiment(user)
# # print(result[0])

# for i,j in result[0].items():
#     print(f"{i} : {j}")




#text generator
print("\ntext generator.....")

text_generator = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")
check = input("Enter what you want to generate ")

result = text_generator(check)

print(result[0]['generated_text'])


