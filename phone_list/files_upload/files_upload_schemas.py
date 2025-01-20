from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *
from fastapi import FastAPI, Query
import datetime


class file_upload_repository(BaseModel):
    files_upload_id : str = Field(...)
    files_upload_name : str = Field(...)
    files_upload_mime : str = Field(...)
    files_upload : List[bytes] = Field(...)
    

    
