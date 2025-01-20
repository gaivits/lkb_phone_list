from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *
from fastapi import FastAPI, Query
import datetime

class users_role_repository(BaseModel):
    
    users_role_name : str = Field(...)
    permissions_id : int = Field(...)

class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10

