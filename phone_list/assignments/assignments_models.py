from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class assignments_model(BaseModel):
    #assignments_id : int
    assignments_type_id : int
    assignments_name : str
    assignments_member : Optional[List[int]] = []
    create_at : Optional[str] = None
    

    
