from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sql.models_alchemy import User, LoanType

class loanBase(BaseModel):
    '''maps a loan table'''
    __tablename__ = 'loans'
    loan_id: int
    user_id: int
    amount: int
    loan_type_id: int
   

class loanCreate(loanBase):
    pass

class loan(loanBase):
    status: Optional[str]
    application_date: datetime
    last_payment_date: Optional[datetime]
    payment_schedule: int
    total_paid: int = 0
    balance: int = 0
    total_amount: int
    loan_type: Optional[LoanType]
    user: Optional[User]    