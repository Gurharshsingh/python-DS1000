"""
FastAPI Backend - Student Management API

HOW TO RUN:
  uvicorn backend:app --reload

OPEN IN BROWSER:
  http://127.0.0.1:8000/docs

CONCEPTS (from mainn.py):
  1. Basic GET route
  2. Path parameters  -> /greet/{name}
  3. Query parameters -> /add?a=10&b=20
  4. Optional query params -> /hello?name=Bob
  5. Pydantic model (data validation)
  6. POST request - receive JSON body
  7. In-memory DB (dict)
  8. Full CRUD - Create, Read, Update, Delete
  9. HTTP errors with HTTPException
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# STEP 1: Create the FastAPI app
app = FastAPI(
    title="Student Management API",
    description="A full CRUD API built with FastAPI - based on mainn.py",
    version="1.0.0",
)

# Allow Streamlit frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# STEP 2: Basic GET route
@app.get("/", tags=["General"])
def home():
    return {"message": "Hello, World! Welcome to FastAPI!", "status": "running"}


# STEP 3: Path Parameter
@app.get("/greet/{name}", tags=["General"])
def greet(name: str):
    return {"message": f"Hello, {name}!"}


# STEP 4: Query Parameters
@app.get("/add", tags=["General"])
def add_numbers(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "result": result}


# STEP 5: Optional Query Parameter
@app.get("/hello", tags=["General"])
def say_hello(name: Optional[str] = "Raj"):
    return {"message": f"Hello, {name}!"}


# STEP 6: Pydantic Model
class Student(BaseModel):
    name: str
    age: int
    grade: str
    marks: float
    is_active: Optional[bool] = True


# STEP 7: In-memory Database
students: dict = {}
next_id: int = 1


# STEP 8: Full CRUD

# CREATE
@app.post("/students", status_code=201, tags=["Students"])
def add_student(student: Student):
    global next_id
    students[next_id] = student.model_dump()
    students[next_id]["id"] = next_id
    result = students[next_id].copy()
    next_id += 1
    return {"message": f"Student '{result['name']}' added successfully!", "student": result}


# READ ALL
@app.get("/students", tags=["Students"])
def get_all_students():
    return {"total": len(students), "students": list(students.values())}


# READ ONE
@app.get("/students/{student_id}", tags=["Students"])
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found!")
    return students[student_id]


# UPDATE
@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found!")
    students[student_id] = student.model_dump()
    students[student_id]["id"] = student_id
    return {"message": "Student updated!", "student": students[student_id]}


# DELETE
@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found!")
    deleted = students.pop(student_id)
    return {"message": f"Student '{deleted['name']}' deleted!", "deleted": deleted}
