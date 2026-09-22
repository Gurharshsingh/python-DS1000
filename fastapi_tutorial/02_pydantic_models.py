"""
=============================================================
 FastAPI Tutorial - Chapter 2: Pydantic Models & Request Body
=============================================================
 TOPICS COVERED:
   1. What is Pydantic?
   2. Creating data models with BaseModel
   3. Sending data in the request body (POST/PUT)
   4. Field validation (required vs optional fields)
   5. Nested models
   6. Response models

 HOW TO RUN:
   >>> uvicorn 02_pydantic_models:app --reload --port 8001

 THEN VISIT:
   - http://127.0.0.1:8001/docs  → Test with Swagger UI
=============================================================
"""

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Chapter 2 - Pydantic Models",
    description="Learn how to use Pydantic models for request/response bodies",
    version="2.0.0"
)


# ==============================================================
# 📌 SECTION 1: Basic Pydantic Model
# ==============================================================
# Pydantic models define the SHAPE and TYPE of your data.
# FastAPI uses them to:
#   ✅ Validate incoming request data
#   ✅ Convert/parse data types automatically
#   ✅ Generate API documentation

class Student(BaseModel):
    """
    A simple Pydantic model for a Student.
    All fields without default values are REQUIRED.
    """
    name: str               # Required field
    age: int                # Required field
    grade: str              # Required field
    is_active: bool = True  # Optional field with default value


# Fake in-memory "database" (a dictionary)
students_db = {}
next_id = 1  # Auto-increment ID


@app.post("/students")
def create_student(student: Student):
    """
    Create a new student.
    
    The 'student: Student' parameter tells FastAPI to:
    1. Read the request body as JSON
    2. Validate it against the Student model
    3. Return a 422 error if validation fails

    Test in Swagger UI with:
    {
        "name": "Alice",
        "age": 20,
        "grade": "A"
    }
    """
    global next_id
    student_dict = student.model_dump()  # Convert Pydantic model to dict
    student_dict["id"] = next_id
    students_db[next_id] = student_dict
    next_id += 1
    return {"message": "Student created!", "student": student_dict}


@app.get("/students")
def get_all_students():
    """Get all students from the database."""
    return {"students": list(students_db.values()), "total": len(students_db)}


@app.get("/students/{student_id}")
def get_student(student_id: int):
    """Get a single student by ID."""
    if student_id not in students_db:
        return {"error": f"Student with id {student_id} not found"}
    return students_db[student_id]


# ==============================================================
# 📌 SECTION 2: Field Validation with Field()
# ==============================================================

class Product(BaseModel):
    """
    Product model.
    """
    name: str
    price: float
    stock: int = 0
    category: str = "general"
    description: str | None = None


products_db = {}
product_next_id = 1


@app.post("/products", status_code=201)  # 201 = Created
def create_product(product: Product):
    """
    Create a new product.
    Pydantic will automatically validate:
    - name must be 2-100 characters
    - price must be > 0
    - stock must be >= 0

    Try sending invalid data to see the error messages!
    Example invalid body:
    { "name": "A", "price": -5 }
    """
    global product_next_id
    product_dict = product.model_dump()
    product_dict["id"] = product_next_id
    products_db[product_next_id] = product_dict
    product_next_id += 1
    return product_dict


# ==============================================================
# 📌 SECTION 3: PUT - Update entire resource
# ==============================================================

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    """
    Update a student completely (all fields replaced).
    HTTP Method: PUT

    PUT replaces the entire resource.
    If student_id doesn't exist, we create it.
    """
    student_dict = student.model_dump()
    student_dict["id"] = student_id
    students_db[student_id] = student_dict
    return {"message": "Student updated!", "student": student_dict}


# ==============================================================
# 📌 SECTION 4: DELETE - Remove a resource
# ==============================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """
    Delete a student by ID.
    HTTP Method: DELETE
    """
    if student_id not in students_db:
        return {"error": f"Student {student_id} not found"}
    deleted = students_db.pop(student_id)
    return {"message": "Student deleted!", "deleted_student": deleted}


# ==============================================================
# 📌 SECTION 5: Nested Models
# ==============================================================

class Address(BaseModel):
    """A nested model for address."""
    street: str
    city: str
    state: str
    pincode: str


class Employee(BaseModel):
    """
    Employee model with a nested Address model.
    This shows how to have complex, nested JSON structures.
    """
    name: str
    email: str
    salary: float
    department: str
    address: Address              # ← Nested model!
    skills: list[str] = []        # ← list field
    joined_at: datetime | None = None


@app.post("/employees")
def create_employee(employee: Employee):
    """
    Create an employee with nested address.

    Test with:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "salary": 50000,
        "department": "Engineering",
        "address": {
            "street": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001"
        },
        "skills": ["Python", "FastAPI", "SQL"]
    }
    """
    return {
        "message": "Employee created!",
        "employee": employee.model_dump()
    }


# ==============================================================
# 📌 SECTION 6: Response Model (Shape the output)
# ==============================================================

class StudentInput(BaseModel):
    """Input model - for receiving data (has all fields)"""
    name: str
    age: int
    grade: str
    password: str  # Sensitive field - don't expose in output!


class StudentOutput(BaseModel):
    """Output model - controls what gets sent in the response"""
    id: int
    name: str
    age: int
    grade: str
    # Notice: no 'password' field! It's hidden from the response.


safe_students_db = {}
safe_next_id = 1


@app.post("/safe-students", response_model=StudentOutput)
def create_safe_student(student: StudentInput):
    """
    The 'response_model=StudentOutput' ensures:
    - Only fields in StudentOutput are returned
    - Password is automatically excluded
    - Response is validated and documented

    This is a security best practice!
    """
    global safe_next_id
    new_student = {
        "id": safe_next_id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade,
        "password": student.password  # stored internally but NOT returned
    }
    safe_students_db[safe_next_id] = new_student
    safe_next_id += 1
    return new_student  # FastAPI filters out 'password' automatically!










