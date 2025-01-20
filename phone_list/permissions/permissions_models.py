from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class permissions_model(BaseModel):
    #permissions_id : int
    creates : int
    updates : int
    looks : int
    deletes : int
    create_at : Optional[str] 
    
    

    
