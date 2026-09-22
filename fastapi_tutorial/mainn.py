#pydantic - basemodel
# post put delete
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title = "Pydantic and POST")

class Student(BaseModel):
    name:str
    age:int     
    grade:str
    is_active:bool=True


db = {} 
next_id = 1 

@app.post("/students")
def create_student(student:Student):
    global next_id
    student_dict = student.model_dump()
    student_dict['id'] = next_id

    db[next_id] = student_dict
    next_id+=1
    return{"message":"Student created", "student":student_dict}


@app.get("/students")
def get_all():
    return{"students": list(db.values()), "total":len(db)}


@app.get("/student/{student_id}")
def get_student(student_id:int):
    if student_id not in db:
        return {"message":f"student {student_id} not found"}
    return db[student_id]




@app.put("/student/{student_id}")
def update_students(student_id :int,student:Student):
    student_dict = student.model_dump()
    student_dict["id"] = student_id
    db[student_id] = student_dict
    return {"message":"Student updated", "student": student_dict}



@app.delete("/students/{students_id}")

def delete_student(student_id : int):
    deleted = db.pop(student_id)
    return{"message":"Student deleted", "delete_student": deleted}



#nested Models

class Address(BaseModel):
    street:str
    city:str
    state:str = "Punjab"
    pincode:str

class Employee(BaseModel):
    name:str
    email:str
    salary:int
    department:str
    address: Address
    joined_at : datetime


@app.post("/employees")
def create_employes(employee:Employee):
    e_dict = employee.model_dump()
    return {"message": "Employee created", "employee":e_dict}


#response model

class AccInput(BaseModel):
    name:str
    age:int
    email:str
    password:str


class AccOutput(BaseModel):
    id:int
    name:str
    age:int
    email:str


new_id = 1

@app.post("/account",response_model=AccOutput)

def create_account(account:AccInput):

    global new_id
    new_acc = account.model_dump()
    new_acc["id"] = new_id
    new_id+=1

    return new_acc