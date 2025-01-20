from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *
import datetime


class users_role_model(BaseModel):
    users_role_name : str
    permissions_id : int
    
