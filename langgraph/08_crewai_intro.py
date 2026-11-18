import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# 2. Configure OpenRouter LLM for CrewAI
llm = LLM(
    model="openrouter/openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.3,
)


# ==========================================================
# 3. Define the Agents (Role-playing personas)
# ==========================================================

# Agent 1: The Researcher
researcher = Agent(
    role="Senior Technology Researcher",
    goal="Uncover cutting-edge developments, facts, and stats on {topic}",
    backstory=(
        "You are an analytical researcher with a passion for emerging technologies. "
        "You extract only verified, high-impact facts and synthesize them clearly."
    ),
    llm=llm,
    verbose=True,
)

# Agent 2: The Writer
writer = Agent(
    role="Lead Technology Writer",
    goal="Turn complex research notes into an engaging, clear summary on {topic}",
    backstory=(
        "You are a skilled tech journalist known for transforming technical research "
        "into captivating, easy-to-read articles that educate and inspire readers."
    ),
    llm=llm,
    verbose=True,
)


# ==========================================================
# 4. Define the Tasks (Work assignments with deliverables)
# ==========================================================

# Task 1: Research assignment
research_task = Task(
    description=(
        "Conduct thorough research on the topic: '{topic}'. "
        "Identify 3 major breakthroughs, benefits, or use cases. "
        "Format your output as clear bullet points."
    ),
    expected_output="A bullet-point list of 3 key facts and takeaways about the topic.",
    agent=researcher,
)

# Task 2: Writing assignment (automatically receives research_task output as context)
writing_task = Task(
    description=(
        "Review the findings provided by the Senior Technology Researcher on '{topic}'. "
        "Write a concise, engaging 2-paragraph article explaining why this matters. "
        "Include a catchy title and a concluding takeaway sentence."
    ),
    expected_output="A polished 2-paragraph article with a title and a key takeaway.",
    agent=writer,
)


# ==========================================================
# 5. Assemble the Crew and Define Process
# ==========================================================

content_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # Task 1 runs first -> its output feeds into Task 2!
    verbose=True,
)


# ==========================================================
# 6. Kickoff the Workflow
# ==========================================================

if __name__ == "__main__":
    topic_input = "Why CrewAI and Multi-Agent Frameworks are Transforming Software"

    print("==========================================")
    print(">> Starting CrewAI Multi-Agent Workflow")
    print(f"Topic: {topic_input}")
    print("==========================================\n")

    # Run the crew
    result = content_crew.kickoff(inputs={"topic": topic_input})

    print("\n==========================================")
    print("[FINAL RESULT FROM CREW]")
    print("==========================================")
    print(result)
