from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sql.models_alchemy import User

from schemas.users import User

class loanType(BaseModel):
    type_name: str
    interest_rate: float
    repayment_period: int
    multiplier: int
    guarantors: Optional[int]

class loanBase(BaseModel):
    '''maps a loan table'''
    amount: int
    loan_type_id: int
    user_id: int
   

class loanCreate(BaseModel):
    # application_date: Optional[datetime]
    amount: int
    loan_type_id: int
    user_id: int
    guarantors: Optional[list[int]]

class Loan(loanBase):
    loan_id: int
    user_id: int
    status: Optional[str]
    application_date: datetime
    last_payment_date: Optional[datetime]
    payment_schedule: int
    total_paid: int = 0
    balance: int = 0
    total_amount: int
    loan_type: Optional[loanType]
    user: Optional[User]

class loan_pay(BaseModel):
    amount: int
    user_id: int
