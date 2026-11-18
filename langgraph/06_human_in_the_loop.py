import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="openrouter/free",
    temperature=0.3,
)

# ==========================================================
# 1. Nodes (Draft -> [Human Approval Breakpoint] -> Send)
# ==========================================================

def draft_email_node(state: dict):
    """Step 1: AI generates an email draft."""
    print("\n--> [Node 1: Drafter] Generating email draft...")
    recipient = state["recipient"]
    topic = state["topic"]

    prompt = f"Write a brief professional email to {recipient} regarding: {topic}"
    response = llm.invoke(prompt)

    return {
        **state,
        "email_draft": response.content.strip(),
        "status": "waiting_for_approval",
    }


def send_email_node(state: dict):
    """Step 2: Executes after human approves."""
    print("\n--> [Node 2: Sender] Executing email dispatch...")
    print(f"    [SENT] Email successfully dispatched to {state['recipient']}!")
    return {
        **state,
        "status": "sent",
    }


# ==========================================================
# 2. Build Graph with Checkpointer (Required for HITL)
# ==========================================================

builder = StateGraph(dict)

builder.add_node("draft_email", draft_email_node)
builder.add_node("send_email", send_email_node)

builder.add_edge(START, "draft_email")
builder.add_edge("draft_email", "send_email")
builder.add_edge("send_email", END)

# Checkpointer saves state per session (thread_id) so we can pause & resume
memory = MemorySaver()

# INTERRUPT BEFORE: Pauses execution right before 'send_email' runs!
app = builder.compile(
    checkpointer=memory,
    interrupt_before=["send_email"]
)


# ==========================================================
# 3. Interactive Human-in-the-Loop Execution
# ==========================================================

if __name__ == "__main__":
    # Every HITL session needs a unique thread_id config
    config = {"configurable": {"thread_id": "session_101"}}

    initial_input = {
        "recipient": "client@example.com",
        "topic": "Project completion and payment reminder"
    }

    print("==========================================")
    print("👤 Human-in-the-Loop (HITL) Workflow")
    print("==========================================")

    # 1. Start execution (Will pause before 'send_email')
    print("\n[Phase 1] Running graph until approval breakpoint...")
    app.invoke(initial_input, config=config)

    # 2. Inspect the paused state
    current_state = app.get_state(config)
    draft = current_state.values["email_draft"]

    print("\n" + "=" * 50)
    print("⏸️  WORKFLOW PAUSED FOR HUMAN REVIEW:")
    print("=" * 50)
    print(draft)
    print("=" * 50)

    # 3. Simulate Human Decision
    print("\nNext Node Scheduled to run:", current_state.next)
    user_choice = input("\nDo you approve sending this email? (yes/no): ").strip().lower()

    if user_choice in ["yes", "y"]:
        print("\n[Phase 2] Human approved! Resuming graph execution...")
        # Resume with None (continues from paused state)
        final_state = app.invoke(None, config=config)
        print("\nStatus:", final_state["status"])
    else:
        print("\n❌ Email cancelled by human supervisor.")
