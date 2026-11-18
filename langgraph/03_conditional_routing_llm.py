import os 
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openrouter import ChatOpenRouter

load_dotenv()

api_key  = os.getenv("OPEN_API_KEY")

llm = ChatOpenRouter(model = "openrouter/free", openrouter_api_key=api_key , temperature=0.6)



def classify_query(state:dict):
    """Node: 1 it uses LLm to classify the user query"""

    print("[NODE-1]")
    user_query = state["query"]

    prompt = (
        f"Classify the following user query into exactly one category. 'billing' or 'technical.\n\n"
        f"Respond ONLY with 'billing' or 'technical'. No other words."
        f"Query : {user_query}"
    )

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    print(f"Selected Category: {category}")

    return {**state, "category": category}


 
def billing_handler(state:dict):
    """NODE 2: Handles billing related queries"""
    print("NODE-2")
    user_input = state["query"]
    prompt = f"You are a billing support assistant. Address the user's billing issue. User Query: {user_input}"

    response = llm.invoke(prompt)
    return {**state, "response": response.content}


def technical_handler(state:dict):
    """Node3 : Handles technical queries"""
    print("[Node3 : Technical Handler]\nHandling Request...")
    prompt = f"""You are a technical support assistant.
    Address the user's technical issue.
    
    User Query: {state['query']}
    """
    response = llm.invoke(prompt)
    return {**state, "response": response.content}


def route_decision (state:dict)->str:
    """This function inspects the state and returns the NAME if the next code.
    It does not update the state, it only decides the direction"""


    if state["category"] == "billing":
        return "billing_node"


    else:
        return "technical_node"


builder = StateGraph(dict)

builder.add_node("classify", classify_query)
builder.add_node("billing_node", billing_handler)
builder.add_node("technical_node", technical_handler)


#edge

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route_decision,{"billing_node":"billing_node", "technical_node":"technical_node"})
builder.add_edge("billing_node",END)
builder.add_edge("technical_node",END)

graph = builder.compile()


input_query = {"query":"My last bill seems too high. Can you please check the details?"}

response = graph.invoke(input_query)
print(response["response"])