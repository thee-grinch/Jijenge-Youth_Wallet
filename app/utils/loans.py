# from fastapi import Depends
from sqlalchemy.orm import session
from dateutil.relativedelta import relativedelta
from datetime import datetime


from sql.models_alchemy import Loan, LoanType
from schemas.loans import loanCreate, loanType

def utilsLoan(Loan):
    '''this class defines all methods for loan class'''
    @property
    def status(self):
        return self.status

def new_loan(loan: loanCreate, user_id: int, db: session):
    # new_loan.update({'user_id', user_id})
    my_loan = {}
    my_loan.update(loan)
    my_loan['user_id'] = user_id
    loan = Loan(**my_loan)
    db.add(loan)
    db.commit()
    return {'message': 'loan created'}

def new_loanType(type_data: loanType, db: session):
    new = {}
    new.update(type_data)
    my_new_type = LoanType(**new)
    db.add(my_new_type)
    db.commit()
    return {'messsage': f'{type_data.type_name} loan was added successfully'}

def calculate_amount(loan: Loan):
    'this function calculates loan amount'
    interest_rate = loan.loan_type.interest_rate / 100
    date_borrowed = loan.application_date
    delta = relativedelta(datetime.now(), date_borrowed)
    print(delta)
    months_borrowed = delta.years * 12 + delta.months or 1
    print(months_borrowed)
    amount_borrowed = loan.amount
    interest = interest_rate * months_borrowed * amount_borrowed
    print(interest)
    setattr(loan, 'total_amount', interest + amount_borrowed)
    return interest + amount_borrowed

    