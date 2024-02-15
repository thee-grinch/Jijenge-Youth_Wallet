from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sql.models_alchemy import User

from schemas.users import User

class loanType(BaseModel):
    type_name: str
    interest_rate: float
    repayment_period: int

class loanBase(BaseModel):
    '''maps a loan table'''
    __tablename__ = 'loans'
    amount: int
    loan_type_id: int
   

class loanCreate(loanBase):
    application_date: Optional[datetime]

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

