import os
import sys
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = LLM(
    model="openrouter/openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.1,
)


# ==========================================================
# 2. Define the Desired Structured Schema (Pydantic)
# ==========================================================
# In production, systems require clean JSON/Pydantic instead of unstructured markdown.

class FeedbackAnalysis(BaseModel):
    product_name: str = Field(description="Name of the product being reviewed")
    sentiment: str = Field(description="Overall sentiment: Positive, Negative, or Mixed")
    satisfaction_score: int = Field(description="Rating from 1 (terrible) to 10 (delighted)")
    key_highlights: List[str] = Field(description="Top 2-3 positive or negative features mentioned")
    recommended_action: str = Field(description="1 immediate action step for customer support or product team")


# ==========================================================
# 3. Define the Analyst Agent
# ==========================================================

analyst = Agent(
    role="Customer Experience Intelligence Specialist",
    goal="Extract actionable structured metrics from raw user reviews for {product}",
    backstory=(
        "You are an expert at customer sentiment analysis. You dissect unstructured "
        "user feedback and turn it into strict, objective diagnostic data."
    ),
    llm=llm,
    verbose=True,
)


# ==========================================================
# 4. Define Task with `output_pydantic`
# ==========================================================

analysis_task = Task(
    description=(
        "Analyze the following customer review for '{product}':\n\n"
        "'''{review_text}'''\n\n"
        "Fill out all fields of the FeedbackAnalysis schema accurately."
    ),
    expected_output="A structured FeedbackAnalysis Pydantic object containing score, sentiment, highlights, and action.",
    agent=analyst,
    output_pydantic=FeedbackAnalysis,  # <-- CrewAI automatically enforces Pydantic validation!
)


# ==========================================================
# 5. Assemble and Run
# ==========================================================

crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    sample_input = {
        "product": "UltraSound Noise-Cancelling Headphones",
        "review_text": (
            "I bought these headphones two weeks ago. The active noise cancellation and sound quality "
            "are phenomenal—easily the best I've heard on flights! However, the headband feels very tight "
            "after 1 hour of wearing, and the companion mobile app crashed twice when updating firmware. "
            "Great hardware, but the app needs serious bug fixes."
        )
    }

    print("==========================================")
    print(">> CrewAI Structured Pydantic Output Demo")
    print(f"Product: {sample_input['product']}")
    print("==========================================\n")

    result = crew.kickoff(inputs=sample_input)

    # CrewAI parses the output into a validated Pydantic model accessible via .pydantic
    parsed_data = result.pydantic

    print("\n==========================================")
    print("[EXTRACTED STRUCTURED DATA]")
    print("==========================================")
    if parsed_data:
        print(f"Product:            {parsed_data.product_name}")
        print(f"Sentiment:          {parsed_data.sentiment}")
        print(f"Satisfaction Score: {parsed_data.satisfaction_score} / 10")
        print(f"Key Highlights:     {', '.join(parsed_data.key_highlights)}")
        print(f"Action Item:        {parsed_data.recommended_action}")
        print("\nRaw JSON Export:")
        print(parsed_data.model_dump_json(indent=2))
    else:
        # Fallback print if LLM output raw text
        print(result.raw)
