from pydantic import BaseModel ,field_validator,Field
from datetime import datetime
from typing import *

import datetime


class registers_repository(BaseModel):
    username : str = Field(...)
    password : str = Field(...)
    full_name : str = Field(...)
    users_role_id : str = Field(...)
    created_at : Optional[str]= None
    updated_at : Optional[str]= None

    

class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10
