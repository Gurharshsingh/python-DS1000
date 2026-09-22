from fastapi import APIRouter,HTTPException

from schemas.models import UserRegister,UserLogin
from database.database import get_connection
from utils import hash_password,verify_password
from jwt_handler import create_access_token

router=APIRouter(prefix='/auth',tags=['Authentication'])


@router.post("/register")
def register(user:UserRegister):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM USERS WHERE EMAIL=?",(user.email,))

    exisiting_user=cursor.fetchone()

    if exisiting_user:
        raise HTTPException(status_code=400,detail="User already exists")
    else:
        hashed_password=hash_password(user.password)
        cursor.execute("INSERT INTO USERS (NAME,EMAIL,PASSWORD) VALUES (?,?,?)",(user.name,user.email,hashed_password))

        conn.commit()
        return {"message":"User registered successfully"}

@router.post("/login")
def login(user:UserLogin):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM USERS WHERE EMAIL=?",(user.email,))

    existing_user=cursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=400,detail="User does not exist")
    else:
        if not verify_password(user.password,existing_user["password"]):
            raise HTTPException(status_code=400,detail="Invalid password")
        else:
            token=create_access_token(data={"user_id":existing_user["id"],"name":existing_user["name"]})
            return {"message":"Login successful","access_token":token,"token_type":"bearer"}
    
