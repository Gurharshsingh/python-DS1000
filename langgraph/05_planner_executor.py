import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openrouter import ChatOpenRouter

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenRouter(model="openrouter/free",openrouter_api_key=api_key,temperature=0.7,)


# node function


# planner, executor, synthesizer


def planner(state:dict):
    """ Step1: Takes user goal and generate 3 step action plan"""

    print("[PLANNER NODE]")

    goal = state["goal"]

    prompt = (
        f"USER GOAL: {goal}\n\n"
        f"Provide a 3 step plan to achive this goal"
        f"Return only 3 steps, seperated by new lines(1 per line)"
    ) 

    response = llm.invoke(prompt)
    steps= response.content.strip().split("\n")[:3]


    print(f"Plan: {steps}")

    return {**state, "plan":steps, "completed_steps":[], "current_step_index":0}


def executor(state:dict):
    """Step2:Executes ONE step at a time"""
    print("[EXECUTOR NODE] Executing next step...")


    index = state["current_step_index"]

    current_task = state["plan"][index]
    print(f"[EXECUTOR NODE] - Executing task #{index+1}: {current_task}")


    prompt = f"Perform this current task in 1-2 sentences: {current_task}"


    response= llm.invoke(prompt)

    step_result = f"step{index+1}({current_task}) : {response.content.strip()}"

    completed = state["completed_steps"] + [step_result]

    return {**state, "completed_steps":completed, "current_step_index": index + 1}
    

def synthesizer(state:dict):
    """Step 3:Combines all results into a coherent final response"""
    print("[Synthesizer Node] compiling final report....\n")
    all_findings = "\n\n".join(state["completed_steps"])

    prompt = (f"Goal: {state['goal']}"
    f"Here is the research findingd from all completed steps : \n {all_findings}"
    f"Synthesize this into a pilished summary")


    response = llm.invoke(prompt)

    return{**state, "final_summary":response.content.strip()}



# condtional edge function

def check_progress(state:dict)->str:
    """If there are any more steps in the plan, continue executing, Else to go synthesize"""
    if state["current_step_index"] < len(state["plan"]):
        return "continue_executing"
    else:
        return "finish_plan"


builder = StateGraph(dict)


builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.add_node("synthesizer", synthesizer)


builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_conditional_edges("executor",check_progress,{"continue_executing": "executor", "finish_plan": "synthesizer"} )
builder.add_edge("synthesizer",END)



app = builder.compile()

user_goal = {"goal":"Create a beginer roadmap to learn agentic ai in 2026"}


result = app.invoke(user_goal)
print(result["final_summary"])




