import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Configure LLM
llm = LLM(
    model="openrouter/openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.2,
)


# ==========================================================
# 3. Define a Custom Tool
# ==========================================================
# In CrewAI, any Python function decorated with @tool becomes an agent capability.
# The docstring is CRITICAL: the LLM reads it to decide WHEN and HOW to use the tool!

@tool("Stock Return Calculator")
def calculate_roi(initial_investment: float, years: int, annual_rate: float) -> str:
    """
    Calculates future value and total ROI of an investment.
    Parameters:
    - initial_investment: amount in dollars (e.g., 1000.0)
    - years: number of years (e.g., 5)
    - annual_rate: percentage growth per year as decimal (e.g., 0.10 for 10%)
    """
    future_value = initial_investment * ((1 + annual_rate) ** years)
    profit = future_value - initial_investment
    roi_percent = (profit / initial_investment) * 100
    return (
        f"Initial: ${initial_investment:,.2f} | "
        f"Years: {years} | "
        f"Future Value: ${future_value:,.2f} | "
        f"Total Profit: ${profit:,.2f} | "
        f"ROI: {roi_percent:.1f}%"
    )


# ==========================================================
# 4. Define Agents (One has the calculator tool!)
# ==========================================================

# Agent 1: Quantitative Analyst equipped with the calculator tool
quant_analyst = Agent(
    role="Quantitative Financial Analyst",
    goal="Accurately compute investment returns using the calculation tool for {company}",
    backstory=(
        "You are a math-driven financial analyst. Whenever numbers need calculation, "
        "you ALWAYS use the Stock Return Calculator tool rather than guessing."
    ),
    tools=[calculate_roi],  # <-- Giving the agent a custom tool!
    llm=llm,
    verbose=True,
)

# Agent 2: Wealth Advisor who translates numbers into plain English advice
wealth_advisor = Agent(
    role="Senior Wealth Advisor",
    goal="Synthesize the analyst's numbers into an easy-to-understand client recommendation",
    backstory=(
        "You are a trusted advisor for everyday investors. You explain investment math "
        "in simple, motivating language with practical risks and benefits."
    ),
    llm=llm,
    verbose=True,
)


# ==========================================================
# 5. Define Tasks
# ==========================================================

task_calculate = Task(
    description=(
        "Use the Stock Return Calculator tool to compute the projected 5-year return "
        "for a $5,000 initial investment in {company} assuming an average 12% annual return (annual_rate=0.12). "
        "Provide the exact figures returned by the tool."
    ),
    expected_output="The precise calculation breakdown from the tool (Future value, profit, and ROI).",
    agent=quant_analyst,
)

task_recommend = Task(
    description=(
        "Using the calculated figures from the Quantitative Financial Analyst, write a 2-paragraph "
        "friendly investment recommendation for the client. Include key pros, risks, and a final verdict."
    ),
    expected_output="A 2-paragraph client-friendly investment memo with figures and a final verdict.",
    agent=wealth_advisor,
)


# ==========================================================
# 6. Assemble Crew and Run
# ==========================================================

finance_crew = Crew(
    agents=[quant_analyst, wealth_advisor],
    tasks=[task_calculate, task_recommend],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    inputs = {"company": "TechGrowth ETF"}

    print("==========================================")
    print(">> CrewAI with Custom Tools Demo")
    print(f"Target: {inputs['company']}")
    print("==========================================\n")

    result = finance_crew.kickoff(inputs=inputs)

    print("\n==========================================")
    print("[FINAL CLIENT RECOMMENDATION]")
    print("==========================================")
    print(result)
