from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *
from fastapi import FastAPI, Query
import datetime

class staffs_repository(BaseModel):
    
    staffs_firstname : str = Field(...,min_length=1)
    staffs_lastname : str = Field(...,min_length=1)
    staffs_username : str = Field(...,min_length=1,max_length=12)
    staffs_phone : str = Field(...,min_length=1)
    #staffs_assignment_id  : int = Field(...)
    permissions_id : Optional[int] = Field(...)
    create_at : Optional[str] = None
    update_at : Optional[str] = None
    
    @field_validator("staffs_phone")
    def phone_is_thai(cls,values):
        return validate_phone(values)

class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10

