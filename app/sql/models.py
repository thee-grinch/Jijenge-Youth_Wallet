from sqlmodel import SQLModel, create_engine, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class User(SQLModel, table=True):
    """maps the table users"""
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: Optional[str]
    first_name: str
    last_name: str
    email: str
    is_verified: bool = Field(default=False)
    registration_date: Optional[datetime] = Field(default=datetime.now())
    last_login_date : Optional[datetime] = Field(default=datetime.now())
    savings: Optional[List['Saving']] = Relationship(back_populates='user')
    contributions: Optional[List['Contribution']] = Relationship(back_populates='user')
    loans: Optional[List['Loan']] = Relationship(back_populates='user')

class Administrator(SQLModel, table=True):
    """maps the table administrators"""
    __tablename__ = 'administrators'
    admin_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    title: str

class Contribution(SQLModel, table=True):
    '''represents the contributiontable'''
    __tablename__ = 'contributions'
    contribution_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    amount: int
    contribution_date: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    user: User = Relationship(back_populates='contributions')
class LoanType(SQLModel, table=True):
    '''maps a loantype'''
    __tablename__ = 'loantypes'
    type_name: str
    loan_type_id: Optional[int] = Field(default=None, primary_key=True)
    interest_rate: float
    repayment_period: int
    loans: Optional[list['Loan']] = Relationship(back_populates='loan_type')

class Loan(SQLModel, table=True):
    '''maps a loan table'''
    __tablename__ = 'loans'
    loan_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    amount: int
    loan_type_id: Optional[int] = Field(default=None, foreign_key='loantypes.loan_type_id')
    status: Optional[str] = 'pending'
    application_date: Optional[datetime] = Field(default=datetime.utcnow())
    last_payment_date: datetime or None = None
    payment_schedule: int
    total_paid: int = 0
    balance: int = 0
    total_amount: int or None = None
    loan_type: Optional[LoanType] = Relationship(back_populates='loans')
    user: User = Relationship(back_populates='loans')
class Saving(SQLModel, table=True):
    '''a savings table mapping'''
    __tablename__ = 'savings'
    saving_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    amount: int
    balance: Optional[int]
    user: User = Relationship(back_populates='savings')

    
