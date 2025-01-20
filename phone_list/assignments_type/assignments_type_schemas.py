from pydantic import BaseModel ,field_validator,Field
from datetime import datetime
from typing import *

import datetime


class assignments_type_repository(BaseModel):
    #assignments_type_id : int
    assignments_type_name : str =  Field(...,min_length=1)
    assignments_type_desc : str = Field(...,min_length=1)
    create_at : Optional[str] = None
    
class query_params(BaseModel):
    pages : Optional[int] = 1
    limits : Optional[int] = 10

    
