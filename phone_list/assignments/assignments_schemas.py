from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from typing import *

import datetime


class assignments_repository(BaseModel):
    #assignments_id : int 
    assignments_type_id : int = Field(...)
    assignments_name : str = Field(...)
    assignments_member : Optional[List[int]] = []
    create_at : Optional[str] = None
    

    
class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10