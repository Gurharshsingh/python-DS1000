import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable

# Ensure console supports all UTF-8 characters from LLMs
sys.stdout.reconfigure(encoding="utf-8")

# 1. Load Environment Variables from .env
load_dotenv()

# 2. Configure LangSmith Tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "Live-Agent-Tracing")

# 3. Initialize the Real LLM (OpenRouter)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_API_KEY"),
    model="openrouter/free",
    temperature=0.3
)

# 4. Custom Pre-processing Tool traced in LangSmith
@traceable(name="clean_user_input", run_type="parser")
def clean_input(query: str) -> str:
    return query.strip()

# 5. Build the Real LangChain Pipeline
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an Enterprise AI Support Agent. Answer questions accurately and concisely in 2 sentences."),
    ("user", "{question}")
])
chain = prompt | llm | StrOutputParser()

# 6. End-to-End Traced Function
@traceable(name="support_agent_workflow")
def run_agent(question: str):
    cleaned_q = clean_input(question)
    response = chain.invoke({"question": cleaned_q})
    return response

# 7. Run Real Invocation
if __name__ == "__main__":
    print("=== Sending Real Query to LLM with LangSmith Tracing ===")
    user_question = "Create a road map for agentic ai in a detailed manner"
    print(f"Question: {user_question}\n")
    
    answer = run_agent(user_question)
    
    print("--- Real Model Answer ---")
    print(answer)
    print("\n[OK] Run logged to LangSmith! View your full trace tree at:")
    print("https://smith.langchain.com -> Project: Live-Agent-Tracing")
