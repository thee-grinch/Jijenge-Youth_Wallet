from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    is_verified = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=datetime.now)
    last_login_date = Column(DateTime, default=datetime.now)
    savings = relationship("Saving", back_populates='user')
    contributions = relationship("Contribution", back_populates='user')
    loans = relationship("Loan", back_populates='user')


class Administrator(Base):
    __tablename__ = 'administrators'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)

class Contribution(Base):
    __tablename__ = 'contributions'
    contribution_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    contribution_date = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates='contributions')

class LoanType(Base):
    __tablename__ = 'loantypes'
    loan_type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String)
    interest_rate = Column(Float)
    repayment_period = Column(Integer)
    loans = relationship("Loan", back_populates='loan_type')

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
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
    loan_type = relationship("LoanType", back_populates='loans')
    user = relationship("User", back_populates='loans')

class Saving(Base):
    __tablename__ = 'savings'
    saving_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    balance = Column(Integer)
    user = relationship("User", back_populates='savings')
