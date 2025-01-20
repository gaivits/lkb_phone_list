import re
from fastapi import Request, HTTPException, status, Depends,Path
from pydantic import EmailStr, ValidationError
from typing import *
from datetime import datetime, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def access_denied(request: Request):
    # This condition checks if the request is for the root path ("/") and is either GET or POST
    if request.url.path == "/" and request.method in ["GET", "POST"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )

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

# Email validation function using Pydantic's built-in EmailStr
def validate_email(email: str) -> str:
    try:
        EmailStr.validate(email)
        return email
    except ValidationError:
        raise ValueError("Invalid email format")

# Phone number validation function using regex


def validate_phone(phone: str) -> str:
    # Example regex for phone numbers (modify based on your needs)
    phone_regex = r"((\+66\s*)?0[\s-]*([0-9][\s-]*){9})"  
    if not re.match(phone_regex, phone):
        raise ValueError("Invalid phone number format")
    return phone


def validate_date_format(create_at: Optional[str]) -> datetime:
    if create_at is None:
        # If create_at is not provided, default to the current datetime
        # Use timezone-aware UTC datetime
        return datetime.now(timezone.utc)

    # Handle custom format if provided as a string
    try:
        return datetime.strptime(create_at, "%Y-%m-%d %H:%M:%S")  # Custom format check
    except ValueError:
        raise ValueError('Invalid datetime format. Expected format: YYYY-MM-DD HH:MM:SS')

    return create_at


def validate_not_empty(value: str) -> str:
    if not value or not value.strip():
        raise ValueError('Field cannot be empty')
    return value

def validate_price(value: float) -> float:
    try:
        # Ensure the value is either a float or integer
        value = float(value)
    except ValueError:
        raise ValueError("Field must be a number")

    if value < 0:
        raise ValueError('Field must be a positive number')

    return value