from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class assignments_type_model(BaseModel):
    assignments_type_id : int
    assignments_type_name : str
    assignments_type_desc : str
    create_at : Optional[str]
    

    
