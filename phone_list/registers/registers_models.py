from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class registers_model(BaseModel):
    id : int
    username : str
    password : str
    full_name : str
    created_at : Optional[str]
    updated_at : Optional[str]

    
