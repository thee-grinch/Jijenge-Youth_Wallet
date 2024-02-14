from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
# from schemas.loans import Loan
# from schemas.user import User

class Administrator(BaseModel):
    admin_id: int
    user_id: int
    title: str

class Contribution(BaseModel):
    contribution_id: int
    user_id: int
    amount: int
    contribution_date: datetime = Field(default_factory=datetime.utcnow)

class LoanType(BaseModel):
    loan_type_id: int
    type_name: str
    interest_rate: float
    repayment_period: int

class Loan(BaseModel):
    loan_id: int
    user_id: int
    amount: int
    loan_type_id: int
    status: str = 'pending'
    application_date: datetime = Field(default_factory=datetime.utcnow)
    last_payment_date: datetime
    payment_schedule: int
    total_paid: int = 0
    balance: int = 0
    total_amount: int
    loan_type: LoanType
    # user: User

class Saving(BaseModel):
    saving_id: int
    user_id: int
    amount: int
    balance: int

class User(BaseModel):
    id: int
    name: str
    password: str
    first_name: str
    last_name: str
    email: str
    is_verified: bool = False
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    last_login_date: datetime = Field(default_factory=datetime.utcnow)
    savings_id: Optional[int]
    contributions_id: Optional[int]
    loans_id: Optional[int]
    savings: Optional[Saving]
    contributions: Optional[List[Contribution]]
    loans: Optional[List[Loan]]