import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openrouter import ChatOpenRouter

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

llm = ChatOpenRouter(model="openrouter/free",openrouter_api_key=api_key,temperature=0.7,)





#node functions

def generator_node(state:dict):
    """Generate initial draft or revise based on critique feedback"""

    revision = state.get("revision_count",0) + 1
    print(f"[GENERATOR NODE]\n Generating Draft (Attempt #({revision}))")

    topic = state["topic"]
    critique = state.get("critique","")

    if critique:

        prompt= (
            f"Topic: {topic}\n"
            f"Previous Draft: {state['draft']}\n"
            f"Critique:{critique}\n"
            f" Please revise and improve the draft adressing the critique"

        )

    else:
        prompt= f"Write a short engaging and 2 sentence tweet about '{topic}'"


    response = llm.invoke(prompt)

    return{**state, "draft":response.content.strip(), "revision_count":revision}


def critic_node(state:dict):
    """Reviews the draft with either approve or tells if it needs revision"""
    print("[CRITIC NODE]\n Analysing Draft...")
    draft = state["draft"]

    prompt = (
        f"Review this tweet: {draft}\n\n"
        f"Criteria: It must have emojis, be under 150 characters, and have a call to action"
        f"If it meets all criteria, reply with ONLY the word APPROVED"
        f"Otherwise, give 1 specific sentence on how to fix it"
    )

    response = llm.invoke(prompt)
    review = response.content.strip()

    if "APPROVED" in review.upper():
        print("Critic Feedback: APPROVED")
        status = "approved"



    else:
        print("Critic Feedback: Needs Revision \n ", review)
        status = "revise"

    return {**state, "critique": review, "status": status}




def should_continue(state:dict)->str:
    """Loop back if needs revision or finish if it is approved"""
    if state["status"] == "approved" or state["revision_count"] >= 2:
        return "finish"
    else:
        return "revise"



builder = StateGraph(dict)


builder.add_node("generate", generator_node)
builder.add_node("critic", critic_node)



builder.add_edge(START, "generate")
builder.add_edge("generate", "critic")

builder.add_conditional_edges(
    "critic",
    should_continue,
    {
        "revise": "generate",
        "finish": END
    }


)


app = builder.compile()


input = {"topic": "Why learning langgraph is important for ai developers"}

print("===========================================")
print(f"Topic: {input}")
print("===========================================")


result = app.invoke(input)


print(result["draft"])
print(f"total revision: {result['revision_count']}")






    