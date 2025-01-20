from pydantic import BaseModel ,field_validator
from datetime import datetime
from typing import *

import datetime


class files_upload_model(BaseModel):
    files_upload_id : str
    files_upload_name : str
    files_upload_mime : str
    files_upload : List[bytes]  
    

    
