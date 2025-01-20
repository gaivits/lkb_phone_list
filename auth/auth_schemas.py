from pydantic import BaseModel
from typing import List


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user_id: int
    username: str
    full_name: str
    user_rule: List[str]
