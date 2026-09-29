from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str