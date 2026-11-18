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

llm = LLM(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.5,
)



# Agent 1 

copywriter = Agent(
    role = "Senior Social media copywriter",
    goal = "Write a viral, compelling linkedin post announcing{announcement} ",
    backstory = ("You creft catchy and professional linkedin and twitter posts that get massive engagement"
                "You use catchy hooks, relevant hashtags, clear call to action"),
    llm  = llm,
    verbose =True    
)


#tast 1 

draft_post_task  = Task(
    description  = ("Write a compelling Linkedin post announcing {announcement}\n\n"
                   "Keep it engaging for tech professionals\n"
                   "Include emojis and line breaks for readability\n"
                   "Use relevant hashtags"),
    expected_output = "A ready to publish linkedin post with emojis and hashtags",
    agent = copywriter,
    human_input = True    
)

marketing_crew = Crew(
    agensts = [copywriter],
    tasks = [draft_post_task],
    process = Process.sequential,
    verbose = True,
)


if __name__ == "__main__":
    campaign_input = {
        "announcement": "We just integrated autonomous Multi-Agent AI workflows into our platform, saving teams 20 hours/week!"
    }

    print("==========================================")
    print(">> CrewAI Human-in-the-Loop (HITL) Workflow")
    print(f"Announcement: {campaign_input['announcement']}")
    print("NOTE: The system will pause and ask for your feedback before finalizing.")
    print("==========================================\n")

    result = marketing_crew.kickoff(inputs=campaign_input)

    print("\n==========================================")
    print("[FINAL APPROVED POST]")
    print("==========================================")
    print(result)
