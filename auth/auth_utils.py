import os
from fastapi import FastAPI, Depends, HTTPException, status,Request,APIRouter,Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import pymysql
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
import time
from collections import deque
from functools import wraps
from auth.auth_models import *
from dotenv import load_dotenv


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT')),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME')
    )


# def rate_limiter(time_frame: int, max_calls: int):
#     def decorator(func):
#         calls = deque()

#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             current_time = time.time()

#             while calls and current_time - calls[0] > time_frame:
#                 calls.popleft()

#             if len(calls) >= max_calls:
#                 raise Exception(f"Rate limit exceeded: {max_calls} requests per {time_frame} seconds.")
            
#             calls.append(current_time)
            
#             return func(*args, **kwargs)

#         return wrapper
#     return decorator

def verify_credentials(username: str, password: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM backend_users WHERE username = %s AND pwd = %s",
                (username, password),
            )
            user = cursor.fetchone()
            if user:
                return user
            else:
                return None
    finally:
        conn.close()


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=os.environ.get('ALGORITHM'))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


def login_for_access_token(form_data: User):
    user = verify_credentials(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token_expires = timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





