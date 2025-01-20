from pydantic import BaseModel
from datetime import datetime
from typing import *

class StaffInfo(BaseModel):
    id: int
    username: str
    full_name: str
    pwd: str
    disabled: int
    create_at: datetime