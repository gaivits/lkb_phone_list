from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *
from fastapi import FastAPI, Query
import datetime

class permissions_repository(BaseModel):
    
    #permissions_id : int
    creates : int = Field(...)
    updates : int= Field(...)
    looks : int= Field(...)
    deletes : int= Field(...)
    
    create_at : Optional[str] = None
   

class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10

