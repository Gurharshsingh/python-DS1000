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

# 2. Configure OpenRouter LLM
llm = LLM(
    model="openrouter/openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.3,
)



architect = Agent(
    role="Senior Software Architect",
    goal="Design a scalable, clean system architecture for {project_idea}",
    backstory=(
        "You are a veteran software architect. You specify data flows, "
        "database schemas, and core backend components with modular precision."
    ),
    llm=llm,
    verbose=True,
)

security_specialist = Agent(
    role="Cybersecurity & QA Specialist",
    goal="Identify potential security vulnerabilities and create test cases for {project_idea}",
    backstory=(
        "You are an ethical hacker and QA lead. You look for auth bypasses, "
        "data leaks, rate limiting issues, and edge-case failure modes."
    ),
    llm=llm,
    verbose=True,
)



architecture_task = Task(
    description=(
        "Design a high-level system architecture for '{project_idea}'. "
        "Outline 3 core backend components and the database choice. Keep it concise."
    ),
    expected_output="A bullet-point architecture breakdown with components and database choice.",
    agent=architect,  # Assigned specialist (Manager oversees and approves)
)

security_task = Task(
    description=(
        "Review the proposed architecture for '{project_idea}' and provide 3 key "
        "security precautions and test strategies to prevent vulnerabilities."
    ),
    expected_output="3 concrete security considerations and validation checks.",
    agent=security_specialist,
)


engineering_crew = Crew(
    agents=[architect, security_specialist],
    tasks=[architecture_task, security_task],
    process=Process.hierarchical, 
    manager_llm=llm,               
    verbose=True,
)



if __name__ == "__main__":
    project_input = {
        "project_idea": "A Multi-Tenant SaaS Billing and Invoicing Engine"
    }

    print("==========================================")
    print(">> Starting Hierarchical CrewAI Workflow")
    print(f"Project: {project_input['project_idea']}")
    print("==========================================\n")

    result = engineering_crew.kickoff(inputs=project_input)

    print("\n==========================================")
    print("[FINAL MANAGER-APPROVED SPECIFICATION]")
    print("==========================================")
    print(result)
