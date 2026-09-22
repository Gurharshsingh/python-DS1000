"""
=============================================================
 FastAPI Tutorial - Chapter 3: HTTP Status Codes & Error Handling
=============================================================
 TOPICS COVERED:
   1. HTTP Status Codes (200, 201, 404, 400, 422, 500)
   2. HTTPException - raising errors properly
   3. Custom Exception Handlers
   4. Response with status_code
   5. JSONResponse

 HOW TO RUN:
   >>> uvicorn 03_status_codes:app --reload

 THEN VISIT:
   - http://127.0.0.1:8002/docs
=============================================================
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel


app = FastAPI(
    title="Chapter 3 - Status Codes & Error Handling",
    version="3.0.0"
)

# ==============================================================
# 📌 COMMON HTTP STATUS CODES REFERENCE:
# ==============================================================
# 200 OK           → Request succeeded
# 201 Created      → Resource was created
# 204 No Content   → Success but no body returned
# 400 Bad Request  → Client sent invalid data
# 401 Unauthorized → Not logged in
# 403 Forbidden    → Logged in but no permission
# 404 Not Found    → Resource doesn't exist
# 409 Conflict     → Duplicate resource / conflict
# 422 Unprocessable → Validation failed (FastAPI default for bad input)
# 500 Internal     → Server-side error
# ==============================================================


# Fake database
items_db = {
    1: {"id": 1, "name": "Laptop",  "price": 999.99},
    2: {"id": 2, "name": "Phone",   "price": 499.99},
    3: {"id": 3, "name": "Tablet",  "price": 299.99},
}


# ==============================================================
# 📌 SECTION 1: Default 200 OK Response
# ==============================================================

@app.get("/items")
def get_all_items():
    """Returns all items. Default status: 200 OK"""
    return {"items": list(items_db.values())}


# ==============================================================
# 📌 SECTION 2: Raising HTTPException (404 Not Found)
# ==============================================================

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Get item by ID.
    
    ✅ If found: returns item with 200 OK
    ❌ If not found: raises 404 HTTPException

    Try: /items/1  → success
    Try: /items/999 → 404 error
    """
    if item_id not in items_db:
        # HTTPException properly formats the error as JSON
        raise HTTPException(
            status_code=404,
            detail=f"Item with id {item_id} not found. Available IDs: {list(items_db.keys())}"
        )
    return items_db[item_id]


# ==============================================================
# 📌 SECTION 3: 201 Created for POST
# ==============================================================

class ItemCreate(BaseModel):
    name: str
    price: float


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """
    Create a new item.
    Returns 201 Created (not the default 200 OK).
    
    Using status.HTTP_201_CREATED is better than magic numbers!
    It's readable and less error-prone.
    """
    new_id = max(items_db.keys()) + 1
    new_item = {"id": new_id, "name": item.name, "price": item.price}
    items_db[new_id] = new_item
    return new_item


# ==============================================================
# 📌 SECTION 4: 409 Conflict - Duplicate Resource
# ==============================================================

users_db = {}

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    """
    Register a new user.
    Returns 409 if username already exists.
    """
    # Check if username already exists
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user.username}' already taken. Choose another."
        )
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{user.email}' is already registered."
            )
    
    users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": "***HASHED***"  # Never store plain passwords!
    }
    return {"message": f"User '{user.username}' registered successfully!"}


# ==============================================================
# 📌 SECTION 5: 400 Bad Request - Invalid Input Logic
# ==============================================================

class AgeVerification(BaseModel):
    name: str
    age: int


@app.post("/verify-age")
def verify_age(data: AgeVerification):
    """
    Verifies if a user meets minimum age requirement.
    Returns 400 if age is invalid (logically wrong, not type-wrong).
    
    Note: Pydantic handles type validation automatically (422).
    But business logic errors should be 400.
    """
    if data.age < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Age cannot be negative!"
        )
    if data.age > 150:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid age. Please enter a realistic age."
        )
    if data.age < 18:
        return {"name": data.name, "eligible": False, "message": "Must be 18+ years old"}
    return {"name": data.name, "eligible": True, "message": "Age verified! ✅"}


# ==============================================================
# 📌 SECTION 6: 204 No Content - Delete with no response body
# ==============================================================

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """
    Delete an item.
    Returns 204 No Content on success (no response body).
    Returns 404 if item not found.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    del items_db[item_id]
    # When status_code=204, return None (no body)
    return {"message":f"Item {item_id} deleted successfully"}

