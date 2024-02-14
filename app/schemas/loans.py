from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sql.models_alchemy import User

from schemas.all_models import LoanType
from schemas.user import User
class loanBase(BaseModel):
    '''maps a loan table'''
    __tablename__ = 'loans'
    amount: int
    loan_type_id: int
   

class loanCreate(loanBase):
    pass

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
    loan_type: Optional[LoanType]
    user: Optional[User]    