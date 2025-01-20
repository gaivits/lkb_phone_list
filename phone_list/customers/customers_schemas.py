from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *
from fastapi import FastAPI, Query
import datetime

class customers_repository(BaseModel):
    
    customers_firstname : str = Field(...,min_length=1)
    customers_lastname : str = Field(...,min_length=1)
    customers_username : str = Field(...,min_length=1,max_length=12)
    customers_phone : str = Field(...,min_length=1)
    staffs_id : List[Union[int,str]] = Field(...,min_length=1)
    create_at : Optional[str] = None
    update_at : Optional[str] = None
    
    @field_validator("customers_phone")
    def phone_is_thai(cls,values):
        return validate_phone(values)

class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10

