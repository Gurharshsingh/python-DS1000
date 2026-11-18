import os
import sys
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load API Key
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="openrouter/free",
    temperature=0.4,
)


# ==========================================================
# 2. Agent Nodes (3 Specialized Personas)
# ==========================================================

def researcher_agent(state: dict):
    """
    Agent 1: The Researcher
    Role: Gathers factual points and key concepts on the topic.
    """
    print("\n--> [Agent 1: Researcher] Gathering key facts and insights...")
    topic = state["topic"]

    prompt = (
        f"You are a Senior Tech Researcher.\n"
        f"Topic: '{topic}'\n\n"
        f"Provide exactly 3 concise, high-value bullet points summarizing the core facts, "
        f"benefits, and importance of this topic."
    )

    response = llm.invoke(prompt)
    print("    [Researcher] Findings collected successfully.")

    return {
        **state,
        "research_notes": response.content.strip(),
    }


def writer_agent(state: dict):
    """
    Agent 2: The Content Writer
    Role: Uses research notes to compose a structured article.
    """
    print("\n--> [Agent 2: Writer] Drafting article from research notes...")
    topic = state["topic"]
    notes = state["research_notes"]

    prompt = (
        f"You are a Professional Tech Writer.\n"
        f"Topic: '{topic}'\n"
        f"Research Notes from Researcher:\n{notes}\n\n"
        f"Using ONLY the research notes above, write an engaging, 2-paragraph article. "
        f"Include a catchy title and an introductory hook."
    )

    response = llm.invoke(prompt)
    print("    [Writer] Draft completed.")

    return {
        **state,
        "draft": response.content.strip(),
    }


def reviewer_agent(state: dict):
    """
    Agent 3: The Chief Editor / Reviewer
    Role: Reviews tone, polishes clarity, and creates the final publishable version.
    """
    print("\n--> [Agent 3: Reviewer] Reviewing, polishing, and finalizing...")
    draft = state["draft"]

    prompt = (
        f"You are a professional editor. Polish and improve the following tech article for clarity and flow. "
        f"Add a 'Key Takeaway' summary at the bottom:\n\n"
        f"{draft}"
    )

    response = llm.invoke(prompt)
    print("    [Reviewer] Final review complete and approved.")

    return {
        **state,
        "final_article": response.content.strip(),
    }


# ==========================================================
# 3. Build the Multi-Agent Graph (Sequential Collaboration)
# ==========================================================

builder = StateGraph(dict)

# Register the 3 specialized agent nodes
builder.add_node("researcher", researcher_agent)
builder.add_node("writer", writer_agent)
builder.add_node("reviewer", reviewer_agent)

# Define the sequential handoff pipeline
# Flow: START -> Researcher -> Writer -> Reviewer -> END
builder.add_edge(START, "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", END)

# Compile the multi-agent graph
app = builder.compile()


# ==========================================================
# 4. Run the Multi-Agent System
# ==========================================================

if __name__ == "__main__":
    initial_input = {
        "topic": "Why Multi-Agent Systems are the Future of AI Development"
    }

    print("==========================================")
    print(">> Multi-Agent Content Creation Pipeline")
    print(f"Topic: {initial_input['topic']}")
    print("==========================================")

    # Invoke the graph
    result = app.invoke(initial_input)

    print("\n==========================================")
    print("[FINAL PUBLICATION-READY ARTICLE]")
    print("==========================================")
    print(result["final_article"])
