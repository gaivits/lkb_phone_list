from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class customers_model(BaseModel):
    customers_id : int
    customers_firstname : str
    customers_lastname : str
    customers_username : str
    customers_phone : str
    staffs_id : List[Union[int,str]] = []
    creates_at : Optional[str]
    updates_at : Optional[str]

    
