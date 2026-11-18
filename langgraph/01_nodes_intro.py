#pip install langgraph


from langgraph.graph import StateGraph, START, END

#Nodes 


def name_greeting(state:dict):
    return{"message":f"Hello,{state['name']}!"}


def uppercase(state:dict):
    return{"message":state["message"].upper()}



builder = StateGraph(dict)

builder.add_node("step1",name_greeting)
builder.add_node("step2",uppercase)

# Edges: Start -> step-1 -> step2 -> END


builder.add_edge(START,"step1")
builder.add_edge("step1","step2")
builder.add_edge("step2",END)


app = builder.compile()



result  = app.invoke({"name": "Sharan"})


print(result['message'])
