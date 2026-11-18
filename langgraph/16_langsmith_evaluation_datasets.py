import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load API keys from .env
load_dotenv()

# 2. Connect to the Real AI Model
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_API_KEY"),
    model="nvidia/nemotron-3.5-lightning:free"
)

# 3. Test Dataset (Questions & Expected Answers)
dataset = [
    {"question": "What is the capital of Australia?", "expected": "Canberra"},
    {"question": "What programming language was LangGraph built in?", "expected": "Python"},
    {"question": "How many days are in a leap year?", "expected": "366"}
]


print("++++Running Evaluation++++")


score = 0 

for item in dataset:
    question  = item["question"]
    expected = item["expected"]


    prompt = f"Answer in 1 short sentence: {question}"

    answer = llm.invoke(prompt).content.strip()

    if expected.lower() in answer.lower():
        print(f"[PASS]question:  {question}")
        print(f"Expected:{answer}")

        score+=1

    else:
        print(f"[FAIL]question:  {question}")
        print(f"Expected:{answer}")

    print("-"*40)
    print(f" Accuracy: {score/len(dataset)*100} %")







