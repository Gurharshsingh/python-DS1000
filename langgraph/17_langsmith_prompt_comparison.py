import os
import sys
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Ensure console supports all UTF-8 characters from LLMs
sys.stdout.reconfigure(encoding="utf-8")

# 1. Load keys from .env
load_dotenv()

# 2. Connect to the Real LLM
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_API_KEY"),
    model="nvidia/nemotron-3.5-lightning:free",
    temperature=0.2
)

# 3. Two Real Prompt Strategies
prompt_a_template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant. Give a detailed multi-sentence response."),
    ("user", "{topic}")
])

prompt_b_template = ChatPromptTemplate.from_messages([
    ("system", "You are an Executive AI. Give an ultra-concise answer in exactly 1 direct sentence."),
    ("user", "{topic}")
])

chain_a = prompt_a_template | llm | StrOutputParser()
chain_b = prompt_b_template | llm | StrOutputParser()

# 4. Compare Live Responses
if __name__ == "__main__":
    topic = "What is Git and why is it used?"
    print(f"=== Comparing Real LLM Responses for Topic: '{topic}' ===\n")

    # Run Prompt A
    print("Sending Prompt A (Verbose) to LLM...")
    t0 = time.time()
    response_a = chain_a.invoke({"topic": topic})
    time_a = time.time() - t0

    # Run Prompt B
    print("Sending Prompt B (Concise) to LLM...")
    t0 = time.time()
    response_b = chain_b.invoke({"topic": topic})
    time_b = time.time() - t0

    print("\n" + "=" * 60)
    print("RESULT FOR PROMPT A (Verbose):")
    print(response_a.strip())
    print(f"Words: {len(response_a.split())} | Time: {time_a:.2f}s")

    print("\n" + "=" * 60)
    print("RESULT FOR PROMPT B (Concise):")
    print(response_b.strip())
    print(f"Words: {len(response_b.split())} | Time: {time_b:.2f}s")

    print("\n" + "=" * 60)
    words_saved = len(response_a.split()) - len(response_b.split())
    print(f"Outcome: Prompt B saved {words_saved} words (~{words_saved * 2} tokens) and took {time_b:.2f}s vs {time_a:.2f}s!")
