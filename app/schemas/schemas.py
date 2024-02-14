from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[int] = None

class UserOutput(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime.datetime
    class config:
        orm_mode = True
