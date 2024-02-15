from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# from sql.models_alchemy import Contribution, Loan
# from schemas.all_models import *

class userBase(BaseModel):
    """maps the table users"""
    name: str
    first_name: str
    last_name: str
    email: str

    
   
class createUser(userBase):
    password: str

class User(userBase):
    id: int
    is_verified: bool = False
    registration_date: Optional[datetime] = None
    last_login_date: Optional[datetime] = None
    savings_id: Optional[int]  = None
    contributions_id: Optional[int] = None
    loans_id: Optional[int] = None
    # savings: Optional[List['Saving']] = None
    # contributions: Optional[List[Contribution]] = None
    # loans: Optional[List[Loan]] = None

    class Config:
        from_attributes = True
