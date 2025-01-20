from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *
import datetime


class staffs_model(BaseModel):
    staffs_id : int
    staffs_firstname : str
    staffs_lastname : str
    staffs_username : str
    staffs_phone : str
    #staff_assignment_id :int
    permissions_id :  int
    creates_at : Optional[str]
    updates_at : Optional[str]

    
