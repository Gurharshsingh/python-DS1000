from langgraph.graph import StateGraph, START, END 

# step - 1 

# node functions 


def calculate_tax(state:dict):
    print("-----NODE 1- Calculate tax-----")
    tax = state["amount"] *0.10
    total = state["amount"] + tax

    return{ **state, "tax":tax, "total":total}


def apply_discount(state:dict):

    print("---Node 2 - Discount---")
    discount = 15.0 if state["total"] >100 else 0.0
    final_total = state["total"] -discount

    return{**state, "discount":discount, "final_total":final_total}

def assign_shipping (state:dict):
    print("---Node- 3 - Shipping----")
    speed = "Free shipping"if state["final_total"]>=100 else "Standard 50RS"
    return{**state, "shipping":speed}



def generate_invoice(state:dict):
    print("---Node -4 Invoice---")
    summary = (
        f"----------------------------------\n"
        f"INVOICE FOR: {state['customer']}\n"
        f"----------------------------------\n"
        f"Base amount- Rs{state['amount']}\n"
        f"Tax(10%) - +Rs{state['tax']}\n"
        f"Discount-  -Rs{state['discount']}\n"
        f"Final Amount : Rs{state['final_total']}\n"
        f"Shipping: {state['shipping']}\n"
        f"----------------------------------\n"

    )

    return {**state, "invoice":summary}



# step -2 Graph

builder = StateGraph(dict)


builder.add_node("step_tax", calculate_tax)
builder.add_node("step_discount",apply_discount)
builder.add_node("step_shipping", assign_shipping)
builder.add_node("step_invoice", generate_invoice)


builder.add_edge(START, "step_tax")
builder.add_edge("step_tax", "step_discount")
builder.add_edge("step_discount", "step_shipping")
builder.add_edge("step_shipping", "step_invoice")
builder.add_edge("step_invoice", END)


app = builder.compile()


order_input= {"customer":"Aarti", "amount": 500}

result = app.invoke(order_input)
print(result["invoice"])

