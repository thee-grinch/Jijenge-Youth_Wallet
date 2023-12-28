from sqlmodel import SQLModel, create_engine, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """maps the table users"""
    UserId: Optional[int] = Field(default=None, primary_key=True)
    UserName: str
    Password: Optional[str]
    FirstName: str
    LastName: str
    RegistrationDate: Optional[datetime] = Field(default=datetime.utcnow())
    LastLoginDate : Optional[datetime] = Field(default=datetime.utcnow())

class Administrator(SQLModel, table=True):
    """maps the table administrators"""
    AdminId: Optional[int] = Field(default=None, primary_key=True)
    UserId: Optional[int] = Field(default=None, foreign_key='user.UserId')
    Title: str

class Contribution(SQLModel, table=True):
    '''represents the contributiontable'''
    ContributionId: Optional[int] = Field(default=None, primary_key=True)
    UserId: Optional[int] = Field(default=None, foreign_key='user.UserId')
    Amount: int
    ContributionDate: Optional[datetime] = Field(default=datetime.utcnow())

class LoanType(SQLModel, table=True):
    '''maps a loantype'''
    TypeName: str
    LoanTypeId: Optional[int] = Field(default=None, primary_key=True)
    InterestRate: float
    RepaymentPeriod: int

class Loan(SQLModel, table=True):
    '''maps a loan table'''
    LoanId: Optional[int] = Field(default=None, primary_key=True)
    UserId: Optional[int] = Field(default=None, foreign_key='user.UserId')
    Amount: int
    LoanTypeId: Optional[int] = Field(default=None, foreign_key=True)
    Status: str
    ApplicationDate: Optional[datetime] = Field(default=datetime.utcnow())
    PaymentSchedule: int
    TotalPaid: int

class Saving(SQLModel, table=True):
    '''a savings table mapping'''
    SavingId: Optional[int] = Field(default=None, primary_key=True)
    UserId: Optional[int] = Field(default=None, foreign_key='user.UserId')
    Amount: int
    Balance: int

    