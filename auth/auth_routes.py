import os
from fastapi import FastAPI, Depends, HTTPException, status,Request,APIRouter,Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import pymysql
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
import time
from collections import deque
from functools import wraps
from auth.auth_routes import *
from auth.auth_models import *
from auth.auth_utils import *
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/login")
def login_for_access_token(form_data: User,response :Response):
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
    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            sql = "UPDATE backend_users SET access_token = %s WHERE username = %s"
            val = (access_token, form_data.username)
            cursor.execute(sql, val)
            db.commit()
    except pymysql.Error as e:
        db.rollback()
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database update failed")
    finally:
        db.close()
    # Removing cookie setting as it's not recommended for access tokens
    response.set_cookie(key='cookie', value=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}