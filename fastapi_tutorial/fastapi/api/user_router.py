from fastapi import APIRouter,Depends

from auth import get_current_user

router=APIRouter(prefix="/user",tags=["User"])

@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return{
        "message":"Welcome",
        "user":current_user
    }
