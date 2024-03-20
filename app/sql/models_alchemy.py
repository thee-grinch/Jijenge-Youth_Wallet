from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
#implemented
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
    notifications = relationship("Notification", back_populates='user')
    shares = relationship("Share", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
class Administrator(Base):
    __tablename__ = 'administrators'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
#completed
class Contribution(Base):
    __tablename__ = 'contributions'
    contribution_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    contribution_date = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates='contributions')
#completed
class LoanType(Base):
    __tablename__ = 'loantypes'
    loan_type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String)
    interest_rate = Column(Float)
    repayment_period = Column(Integer)
    loans = relationship("Loan", back_populates='loan_type')
#completed
class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    loan_type_id = Column(Integer, ForeignKey('loantypes.loan_type_id'))
    status = Column(String, default='pending')
    application_date = Column(DateTime, default=datetime.now)
    last_payment_date = Column(DateTime)
    payment_schedule = Column(Integer)
    total_paid = Column(Integer, default=0)
    balance = Column(Integer, default=0)
    total_amount = Column(Integer)
    loan_type = relationship("LoanType", back_populates='loans')
    user = relationship("User", back_populates='loans')
    guarantors = relationship("Guarantor", back_populates='loan')

#completed
class Saving(Base):
    __tablename__ = 'savings'
    saving_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    # balance = Column(Integer)
    user = relationship("User", back_populates='savings')

#completed
class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    message = Column(String)
    date = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates='notifications')
#completed
class Guarantor(Base):
    __tablename__ = 'guarantors'

    guarantor_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey('loans.loan_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.now)

    loan = relationship("Loan", back_populates='guarantors')
    # user = relationship("User", back_populates='guarantors')

class Share(Base):
    __tablename__ = 'shares'

    share_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(DECIMAL(10, 2))
    date = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates='shares')

#implemented
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String(50))
    amount = Column(DECIMAL(10, 2))
    date = Column(DateTime , default=datetime.now)
    money_in = Column(Boolean, default=True)

    user = relationship("User", back_populates='transactions')

#implemented
class Total(Base):
    __tablename__ = 'totals'

    id = Column(String(50), primary_key=True)
    date = Column(DateTime, default=datetime.now)
    loans = Column(Integer, default=0)
    savings = Column(Integer, default=0)
    contributions = Column(Integer, default=0) 
    Shares = Column(Integer, default=0)
