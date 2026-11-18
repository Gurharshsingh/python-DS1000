import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="openrouter/free",
    temperature=0,
)

# ==========================================================
# 1. Nodes (Planner -> Executor Loop -> Synthesizer)
# ==========================================================



def planner_node(state:dict):
    """Step1:Takes user goal and generates 3 step action plan"""
    print("[PLANNER NODE]\n Devising a 3 step plan...")
    goal = state["goal"]

    prompt = (
        f"User Goal: {goal}\n\n"
        f"Provide a 3 step plan to achieve this goal"
        f"Return ONLY the 3 steps, seperated by newlines(1 per line)"
        
    )


    response = llm.invoke(prompt)
    steps = response.content.strip().split("\n")[:3]
    print(f"PLAN: {steps}")

    return{
        **state,
        "plan":steps,
        "completed_steps": [], 
        "current_step_index": 0
        
    }



def executor_node(state:dict):
    """Step2:Executes ONE step at a time"""
    print("[EXECUTOR NODE] Executing next step...")
    
    index = state['current_step_index']
    current_task = state['plan'][index]
    print(f"[EXECUTOR NODE] Executing Task #{index +1}: {current_task}")

    prompt = f"Perform this current task in 1-2 sentences : {current_task}"

    response = llm.invoke(prompt)
    
    step_result = f"step{index +1} ({current_task}): {response.content.strip()}"
    completed  = state["completed_steps"] + [step_result]  
    
    return  {
        **state,
        "completed_steps": completed,
        "current_step_index": index + 1,
    }    




def synthesizer_node(state:dict):
    """Step 3:Combines all results into a coherent final response"""
    print("[Synthesizer Node] compiling final report....\n")
    all_findings = "\n\n".join(state["completed_steps"])

    prompt = (
        f"Goal: {state}"
        f"Here is the research findings form all completed steps: \n{all_findings}"
        f"Synthesize this into a polished structured summary")


    response = llm.invoke(prompt)
    return {**state, "final_summary":response.content.strip()}

#router function

def check_plan_progress(state:dict)->str:
    """If there are any more steps in the plan, continue executing, Else to go synthesize"""
    if state["current_step_index"] < len(state["plan"]):
        return "continue_executing"
    return "finish_plan"


builder = StateGraph(dict)


builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("synthesizer", synthesizer_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_conditional_edges(
    "executor",
    check_plan_progress,
    {
        "continue_executing": "executor",
        "finish_plan": "synthesizer"
    }
)

builder.add_edge("synthesizer", END)


app  =  builder.compile()

user_goal  = {"goal":"Create a beginer roadmap to learn agentic ai in 2026"}

result = app.invoke(user_goal)

print("\n\n" + "="*50)
print("FINAL ROADMAP:\n")
print(result["final_summary"])


   
    


    




