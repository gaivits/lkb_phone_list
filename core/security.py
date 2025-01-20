import os
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from mysql.connector import MySQLConnection
from core.db import *
from auth.auth_utils import *

load_dotenv()

# Load secret key and algorithm from environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_access_token_expried(user):
    try:
        payload = jwt.decode(user.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) > datetime.utcnow():
            return user.access_token  # Token is valid
        else:
            raise JWTError  # Token has expired or is invalid
    except JWTError:
        # Generate a new token if the current one has expired or is invalid
        user_project = ["wms", "dmk"]
        token_data = {
            "user_id": user.id,
            "izx_username": user.username,
            "user_project": user_project,
        }
        return create_access_token(data=token_data)


# Get current user by decoding the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
     credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
     )
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])         
         username: str = payload.get("izx_username")
         if username is None:
             raise credentials_exception
     except JWTError:
         raise credentials_exception
     return username



