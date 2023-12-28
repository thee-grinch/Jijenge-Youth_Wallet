from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """this is the class to represent the user table"""

    __tablename__ = 'users'
    
    UserId = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(20), unique=True)
    Password = Column(String(16))
    FirstName = Column(String(10))
    LastName = Column(String(10))
    RegistrationDate = Column(Date)
    LastLoginDate = Column(DateTime)
    Administrator = Column(Boolean)

class Administrator(Base):
    """ class to represent all the administrators"""
    __tablename__ = 'Administrators'

    AdminId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey(users.UserId))
    Title = Column(String(10))

class Contribution(Base):
    """represents all user contributions"""

    __tablename__ = 'contributions'
    
    ContributionId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey(users.UserId))
    Amount = Column(Integer)
    ContributionDate = Column(Date)

class LoanType(Base):
    """represents a loantype table"""

    __tablename__ = 'loanTypes'

    TypeName = Column(String)
    LoanTypeId = Column(Integer, primary_key=True, autoincrement=True)
    InterestRate = Column(Float)
    RepaymentPeriod = Column(Integer)

class Loan(Base):
    """represents the loans table"""

    __tablename__ = "loans"
    LoanId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey(users.UserId))
    Amount = Column(Integer)
    LoanTypeId = Column(Integer, ForeignKey(loanTypes.LoanTypeId))
    Status = Column(String)
    ApplicationDate = Column(Date)
    PaymentShedule = Column(Integer)
    TotalPaid = Column(Integer)

class Saving(Base):
    """Represents a saving class"""
    __tablename__ = 'savings'
    SavingsId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey(users.UserId))
    Amount = Column(Integer)
    Balance = Column(Integer)
