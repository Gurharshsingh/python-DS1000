"""

FastAPI is a modern, fast web framework for building APIs with Python.

HOW TO RUN:
  1. Install dependencies:
       pip install fastapi uvicorn

  2. Run the server:
       uvicorn mainn:app --reload

  3. Open your browser:
       - API:  http://127.0.0.1:8000
       - Docs: http://127.0.0.1:8000/docs   ← Interactive API docs (FREE!)


"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# ─────────────────────────────────────────────
# STEP 1: Create the FastAPI app
# ─────────────────────────────────────────────
app = FastAPI(
    title="My First FastAPI App",
    description="A simple tutorial to learn FastAPI",
    version="1.0.0",
)


# ─────────────────────────────────────────────
# STEP 2: A Basic Route (GET request)
# ─────────────────────────────────────────────
# @app.get("/")  means: "when someone visits the homepage, run this function"
@app.get("/")
def home():
    return {"message": "Hello, World! Welcome to FastAPI 🎉"}


# ─────────────────────────────────────────────
# STEP 3: Route with a Path Parameter
# ─────────────────────────────────────────────
# {name} is a variable in the URL
# Try: http://127.0.0.1:8000/greet/Alice
@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}! 👋"}


# # ─────────────────────────────────────────────
# # STEP 4: Route with a Query Parameter
# # ─────────────────────────────────────────────
# Query params come after "?" in the URL
# Try: http://127.0.0.1:8000/add?a=10&b=20
@app.get("/add")
def add_numbers(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "result": result}


# ─────────────────────────────────────────────
# STEP 5: Optional Query Parameter
# ─────────────────────────────────────────────
# Try: http://127.0.0.1:8000/hello
# Try: http://127.0.0.1:8000/hello?name=Bob
@app.get("/hello")
def say_hello(name: Optional[str] = "Raj"):
    return {"message": f"Hello, {name}!"}


# # ─────────────────────────────────────────────
# STEP 6: Pydantic Model (Data Validation)
# ─────────────────────────────────────────────
# Pydantic automatically validates the data you receive
class Student(BaseModel):
    name: str
    age: int
    grade: str


# ─────────────────────────────────────────────
# STEP 7: POST Request — Receive Data
# ─────────────────────────────────────────────
# POST is used to SEND data to the server
# FastAPI automatically reads JSON from the request body
@app.post("/students")
def create_student(student: Student):
    return {
        "message": f"Student '{student.name}' added successfully!",
        "student": student,
    }

# form -> student name ,age , grade -> post -> stores data in db 




# # ─────────────────────────────────────────────
# # STEP 8: In-memory "Database" (a simple list)
# # ─────────────────────────────────────────────
# # In real apps you'd use a real database (SQLite, PostgreSQL, etc.)
db: list[dict] = []


@app.post("/students/add")
def add_student(student: Student):
    db.append(student.dict())
    return {"message": "Added!", "total_students": len(db)}


@app.get("/students/all")
def get_all_students():
    return {"students": db, "count": len(db)}


# # ─────────────────────────────────────────────
# STEP 9: HTTP Errors — Return proper error codes
# ─────────────────────────────────────────────
# Try: http://127.0.0.1:8000/students/999
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    if student_id < 0 or student_id >= len(db):
        # 404 = Not Found
        raise HTTPException(status_code=404, detail="Student not found!")
    return db[student_id]


# ─────────────────────────────────────────────
# STEP 10: DELETE Request
# ─────────────────────────────────────────────
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id < 0 or student_id >= len(db):
        raise HTTPException(status_code=404, detail="Student not found!")
    removed = db.pop(student_id)
    return {"message": "Deleted!", "removed_student": removed}


# # ─────────────────────────────────────────────
# # QUICK REFERENCE
# # ─────────────────────────────────────────────
# """
# HTTP METHOD  |  PURPOSE          |  Example URL
# -------------|-------------------|----------------------------
# GET          |  Read data        |  /students/all
# POST         |  Create new data  |  /students/add
# PUT          |  Update data      |  /students/5
# DELETE       |  Delete data      |  /students/5

# STATUS CODES:
#   200 = OK (success)
#   201 = Created
#   400 = Bad Request (your fault)
#   404 = Not Found
#   500 = Internal Server Error (server's fault)
# """
