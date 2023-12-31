from sqlmodel import SQLModel, create_engine, Field, Relationship
from typing import Optional
from datetime import datetime, timezone

class User(SQLModel, table=True):
    """maps the table users"""
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    password: Optional[str]
    first_name: str
    last_name: str
    registration_date: Optional[datetime] = Field(default=datetime.now())
    last_login_date : Optional[datetime] = Field(default=datetime.now())

class Administrator(SQLModel, table=True):
    """maps the table administrators"""
    __tablename__ = 'administrators'
    admin_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id')
    title: str

class Contribution(SQLModel, table=True):
    '''represents the contributiontable'''
    __tablename__ = 'contributions'
    contribution_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id')
    amount: int
    contribution_date: Optional[datetime] = Field(default=datetime.now(timezone.utc))
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
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id')
    amount: int
    loan_type_id: Optional[int] = Field(default=None, foreign_key='loantypes.loan_type_id')
    status: str
    application_date: Optional[datetime] = Field(default=datetime.utcnow())
    payment_schedule: int
    total_paid: int
    loan_type: Optional[LoanType] = Relationship(back_populates='loans')

class Saving(SQLModel, table=True):
    '''a savings table mapping'''
    __tablename__ = 'savings'
    saving_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id')
    amount: int
    balance: int

    
