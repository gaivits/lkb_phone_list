from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import *
from datetime import datetime
from dependencies.common import *


class StaffListInTable(BaseModel):
    id: int
    username: str
    full_name: str
    disabled: int
    create_at: Optional[datetime] = None


class StaffListSearchRequest(BaseModel):
    username : Optional[str] = None
    full_name: Optional[str] = None
    status: Optional[str] = None
    orderby_col: str
    orderby_val: str
    page: int
    page_size: int


class AddStaffRequest(BaseModel):
    username: str = Field(..., min_length=1)
    pwd: str = Field(..., min_length=1)
    full_name: str = Field(..., min_length=1)
    disabled: int
    create_at: Optional[datetime] = None

    @field_validator('create_at', mode='before')
    def check_create_at(cls, v):
        return validate_date_format(v)

    @field_validator('username', 'pwd', 'full_name', mode='before')
    def check_not_empty(cls, v):
        return validate_not_empty(v)

    @field_validator('disabled', mode='before')
    def check_integer(cls, v):
        return validate_price(v)


class EditStaffRequest(BaseModel):
    username: str = Field(..., min_length=1)
    pwd: str = Field(..., min_length=1)
    full_name: str = Field(..., min_length=1)
    disabled: int
    update_at: Optional[datetime] = None

    @field_validator('update_at', mode='before')
    def check_create_at(cls, v):
        return validate_date_format(v)

    @field_validator('username', 'pwd', 'full_name', mode='before')
    def check_not_empty(cls, v):
        return validate_not_empty(v)

    @field_validator('disabled', mode='before')
    def check_integer(cls, v):
        return validate_price(v)
