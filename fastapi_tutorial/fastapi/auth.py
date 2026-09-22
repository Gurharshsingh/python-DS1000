from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

from jwt_handler import verify_token

oauth2scheme=OAuth2PasswordBearer(tokenUrl="auth/login")



def get_current_user(token:str=Depends(oauth2scheme)):
    
    payload=verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )
    return payload