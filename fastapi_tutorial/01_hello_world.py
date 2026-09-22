"""
=============================================================
 FastAPI Tutorial - Chapter 1: Hello World & Basics
=============================================================
 TOPICS COVERED:
   1. What is FastAPI?
   2. Creating a FastAPI app
   3. Defining route/endpoints
   4. HTTP Methods: GET, POST, PUT, DELETE
   5. Path Parameters
   6. Query Parameters
   7. Automatic Interactive Docs (Swagger UI)

 HOW TO RUN:
   Open terminal and run:
   >>> uvicorn 01_hello_world:app --reload

 THEN VISIT:
   - http://127.0.0.1:8000           → Main app
   - http://127.0.0.1:8000/docs      → Swagger UI (Interactive Docs)
   
=============================================================
"""

from fastapi import FastAPI

# ✅ Step 1: Create the FastAPI application instance
app = FastAPI(
    title="FastAPI Tutorial",
    description="A beginner-friendly FastAPI teaching project 🚀",
    version="1.0.0"
)

# ==============================================================
# 📌 SECTION 1: Basic GET Route
# ==============================================================

@app.get("/")
def home():
    """
    Root endpoint - returns a welcome message.
    HTTP Method: GET
    URL: http://127.0.0.1:8000/
    """
    return {"message": "Welcome to FastAPI! 🎉", "status": "running"}


@app.get("/about")
def about():
    """
    Returns information about this API.
    HTTP Method: GET
    URL: http://127.0.0.1:8000/about
    """
    return {
        "name": "FastAPI Tutorial",
        "author": "Your Name",
        "version": "1.0.0",
        "description": "Learning FastAPI step by step"
    }


# ==============================================================
# 📌 SECTION 2: Path Parameters
# ==============================================================
# Path parameters are dynamic parts of the URL path.
# They are defined using curly braces {param_name}

@app.get("/greet/{name}")
def greet_user(name: str):
    """
    Greets a user by name.
    Path Parameter: name (string)
    Example URL: http://127.0.0.1:8000/greet/Alice
    """
    return {"message": f"Hello, {name}! Welcome to FastAPI 👋"}


@app.get("/square/{number}")
def square_number(number: int):
    """
    Returns the square of a number.
    Path Parameter: number (integer) — FastAPI auto-validates the type!
    Example URL: http://127.0.0.1:8000/square/5  → returns 25
    Example URL: http://127.0.0.1:8000/square/abc → returns 422 Validation Error
    """
    return {
        "number": number,
        "square": number ** 2,
        "cube": number ** 3
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Simulates fetching an item by ID.
    Example URL: http://127.0.0.1:8000/items/42
    """
    # Fake database
    fake_db = {
        1: "Laptop",
        2: "Phone",
        3: "Tablet",
        42: "Magic Item ✨"
    }
    item = fake_db.get(item_id, "Item Not Found")
    return {"item_id": item_id, "item_name": item}


# ==============================================================
# 📌 SECTION 3: Query Parameters
# ==============================================================
# Query parameters come after '?' in the URL.
# They are function parameters that are NOT path parameters.
# Example: /search?keyword=python&limit=5

@app.get("/search")
def search_items(keyword: str, limit: int = 10, skip: int = 0):
    """
    Search for items. 
    This version is simplified to show exactly how we generate the list of results!
    """
    results = []
    
    # 1. Figure out what number to start at
    start_number = skip + 1
    
    # 2. Figure out what number to end at
    end_number = skip + limit + 1
    
    # 3. Create a fake item for each number in that range
    for i in range(start_number, end_number):
        item_name = f"{keyword} result {i}"
        results.append(item_name)

    # 4. Return our data back to the user
    return {
        "keyword_searched": keyword,
        "results_returned": len(results),
        "results": results
    }


@app.get("/users")
def get_users(active: bool = True, role: str = "student"):
    """
    Get users filtered by active status and role.
    Query Parameters:
        - active (optional, default=True): Filter by active status
        - role (optional, default='student'): Filter by role

    Example URL: http://127.0.0.1:8000/users?active=true&role=admin
    """
    # Simulate filtered users
    all_users = [
        {"id": 1, "name": "Alice", "active": True,  "role": "admin"},
        {"id": 2, "name": "Bob",   "active": True,  "role": "student"},
        {"id": 3, "name": "Carol", "active": False, "role": "student"},
        {"id": 4, "name": "Dave",  "active": True,  "role": "teacher"},
    ]
    filtered = [u for u in all_users if u["active"] == active and u["role"] == role]
    return {"users": filtered, "count": len(filtered)}


# ==============================================================
# 📌 SECTION 4: Combining Path + Query Parameters
# ==============================================================

@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, status: str = "all", limit: int = 5):
    """
    Get orders for a specific user.
    Path Parameter: user_id
    Query Parameters: status, limit

    Example URL: http://127.0.0.1:8000/users/1/orders?status=pending&limit=3
    """
    orders = [
        {"order_id": 101, "item": "Book",   "status": "delivered"},
        {"order_id": 102, "item": "Pen",    "status": "pending"},
        {"order_id": 103, "item": "Laptop", "status": "pending"},
    ]
    if status != "all":
        orders = [o for o in orders if o["status"] == status]
    return {
        "user_id": user_id,
        "status_filter": status,
        "orders": orders[:limit]
    }


# ==============================================================
# 📌 QUICK REFERENCE
# ==============================================================
# @app.get("/path")    → Read data
# @app.post("/path")   → Create data
# @app.put("/path")    → Update data (full)
# @app.patch("/path")  → Update data (partial)
# @app.delete("/path") → Delete data
