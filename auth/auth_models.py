from pydantic import BaseModel, Field, validator, EmailStr
from typing import *
from datetime import datetime

class User(BaseModel):
    username: str
    password: str