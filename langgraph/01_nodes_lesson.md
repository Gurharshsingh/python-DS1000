# Lesson 1: LangGraph Basics (Using Standard Python Dict)

## 📌 The 3 Simple Steps of LangGraph

```
1. Nodes      -> Regular Python functions that take & return a dict
2. Graph      -> StateGraph(dict) + add_node + add_edge
3. Run        -> compile() and invoke()
```

---

## 💻 Complete Starter Code ([01_nodes_intro.py](file:///e:/python-DS1000/langgraph/01_nodes_intro.py))

```python
from langgraph.graph import StateGraph, START, END

# 1. Nodes (functions that do work)
def make_greeting(state: dict):
    return {"message": f"Hello, {state['name']}!"}

def make_uppercase(state: dict):
    return {"message": state["message"].upper()}


# 2. Build the Graph (using standard Python dict)
builder = StateGraph(dict)

builder.add_node("step_1", make_greeting)
builder.add_node("step_2", make_uppercase)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", END)


# 3. Compile and Run
app = builder.compile()

result = app.invoke({"name": "Alice"})
print(result)
```

---

## 🏃 Run It:
```bash
python 01_nodes_intro.py
```

### Output:
```python
{'name': 'Alice', 'message': 'HELLO, ALICE!'}
```

---

## 💡 Key Teaching Concepts:
1. **No Extra Imports Needed**: State is just a standard Python dictionary `dict`.
2. **Node Function Rule**:
   - Takes `state: dict` as input.
   - Returns a dictionary with updated or new key-value pairs.
3. **Graph Flow**:
   - `START ➔ step_1 ➔ step_2 ➔ END`
