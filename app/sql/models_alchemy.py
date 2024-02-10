from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional, List, a
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    """maps the table users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    is_verified = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=func.now())
    last_login_date = Column(DateTime, default=func.now())
    savings_id = Column(Integer, ForeignKey('savings.saving_id'))
    contributions_id = Column(Integer, ForeignKey('contributions.contribution_id'))
    loans_id = Column(Integer, ForeignKey('loans.loan_id'))
    savings = relationship("Saving", back_populates="user")
    contributions = relationship("Contribution", back_populates="user")
    loans = relationship("Loan", back_populates="user")

class Administrator(Base):
    """maps the table administrators"""
    __tablename__ = 'administrators'
    admin_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)

class Contribution(Base):
    '''represents the contributiontable'''
    __tablename__ = 'contributions'
    contribution_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    contribution_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="contributions")

class LoanType(Base):
    '''maps a loantype'''
    __tablename__ = 'loantypes'
    loan_type_id = Column(Integer, primary_key=True)
    type_name = Column(String)
    interest_rate = Column(Float)
    repayment_period = Column(Integer)
    loans = relationship("Loan", back_populates="loan_type")

class Loan(Base):
    '''maps a loan table'''
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    loan_type_id = Column(Integer, ForeignKey('loantypes.loan_type_id'))
    status = Column(String, default='pending')
    application_date = Column(DateTime, default=datetime.utcnow)
    last_payment_date = Column(DateTime)
    payment_schedule = Column(Integer)
    total_paid = Column(Integer, default=0)
    balance = Column(Integer, default=0)
    total_amount = Column(Integer)
    loan_type = relationship("LoanType", back_populates="loans")
    user = relationship("User", back_populates="loans")

class Saving(Base):
    '''a savings table mapping'''
    __tablename__ = 'savings'
    saving_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    balance = Column(Integer)
    user = relationship("User", back_populates="savings")