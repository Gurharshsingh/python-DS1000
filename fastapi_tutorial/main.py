"""
=============================================================
 FastAPI - Today's Class 🎓
 Topic: One Pydantic Model + Basic CRUD
=============================================================
 HOW TO RUN:
   Open terminal and type:
   >>> uvicorn main:app --reload

 OPEN IN BROWSER:
   http://127.0.0.1:8000/docs   ← Interactive API testing
=============================================================
"""

from logging import info
# fast api- back end 
# requests - server
# get - get info
# post - add that info to server
# put - update that info 
# delete - delete that info








from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ✅ Step 1: Create the app
app = FastAPI(title="Student API")


# ✅ Step 2: Define ONE model (the shape of our data)
class Student(BaseModel):
    name: str
    age: int
    grade: str
    marks: float
    is_active: bool | None = True      # Optional → has a default value


# ✅ Step 3: In-memory database (just a dictionary for now)
students = {}
next_id = 1


# ──────────────────────────────────────────
# CREATE  → POST /students
# ──────────────────────────────────────────
@app.post("/students", status_code=201)
def add_student(student: Student):
    global next_id
    students[next_id] = student.model_dump()
    students[next_id]["id"] = next_id
    next_id += 1
    return {"message": "Student added!", "student": students[next_id - 1]}


# ──────────────────────────────────────────
# READ ALL  → GET /students
# ──────────────────────────────────────────
@app.get("/students")
def get_all_students():
    return {"total": len(students), "students": list(students.values())}


# ──────────────────────────────────────────
# READ ONE  → GET /students/{id}
# ──────────────────────────────────────────
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


# ──────────────────────────────────────────
# UPDATE  → PUT /students/{id}
# ──────────────────────────────────────────
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student.model_dump()
    students[student_id]["id"] = student_id
    return {"message": "Student updated!", "student": students[student_id]}


# ──────────────────────────────────────────
# DELETE  → DELETE /students/{id}
# ──────────────────────────────────────────
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    deleted = students.pop(student_id)
    return {"message": "Student deleted!", "deleted": deleted}
