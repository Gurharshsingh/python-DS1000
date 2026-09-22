from pydantic import BaseModel,EmailStr

class Item(BaseModel):
    id:int
    name:str
    price:float
    tax:float

class UserRegister(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    id:int
    full_name:str
    email:EmailStr

class UserLogin(BaseModel):
    email:EmailStr
    password:str

