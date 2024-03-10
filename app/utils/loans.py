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
def verify_loan(loan: Loan):
    loan.status = 'verified'

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
    # total_amount = loan.total_amount
    delta = relativedelta(datetime.now(), date_borrowed)
    # print(delta)
    months_borrowed = delta.years * 12 + delta.months or 1
    # print(months_borrowed)
    amount_borrowed = loan.amount
    interest = interest_rate * months_borrowed * amount_borrowed
    # print(interest)
    setattr(loan, 'total_amount', interest + amount_borrowed)
    return interest + amount_borrowed

def set_balance(loan: Loan):
    bal = loan.balance
    paid = loan.total_paid
    if loan.status != 'paid':
        total_amount = loan.total_amount
        if loan.balance == 0:
            setattr(loan, 'balance', total_amount)
        else:
            setattr(loan, 'balance', total_amount - paid)

def calculate_amount_and_set_balance(loan: Loan):
    interest_rate = loan.loan_type.interest_rate / 100
    date_borrowed = loan.application_date
    # total_amount = loan.total_amount
    delta = relativedelta(datetime.now(), date_borrowed)
    months_borrowed = delta.years * 12 + delta.months or 1
    amount_borrowed = loan.amount
    interest = interest_rate * months_borrowed * amount_borrowed
    loan.total_amount = interest + amount_borrowed
    loan.balance = loan.total_amount if loan.balance == 0 else loan.total_amount - loan.balance

def pay_loan(loan: Loan, amount_paid: int):
    if loan.status == 'paid':
        raise ValueError('already paid')
    if amount_paid <= 0:
        raise ValueError('you cant pay zero amount')
    total_paid = loan.total_paid
    bal = loan.balance
    if amount_paid > bal:
        raise ValueError('amount greater than the loan balance')

    total_amount = loan.total_amount

    total_paid += amount_paid
    bal = total_amount - total_paid
    setattr(loan, 'balance', bal)
    setattr(loan, 'total_paid', total_paid)
    setattr(loan, 'last_payment_date', datetime.now())
    return {'loan paid successfully'}

def calculate_repayment_schedule(loan: Loan):
    total_amount = loan.total_amount
    repayment_period = loan.loan_type.repayment_period
    print(repayment_period)
    # end_date = loan.application_date + relativedelta(months=repayment_period)
    date_elapsed = relativedelta(datetime.now(), loan.application_date).months
    # print(date_elapsed)
    remaining_months = repayment_period - date_elapsed
    # print(remaining_months)
    # remaining_months = relativedelta(end_date, datetime.now()).months or 1
    setattr(loan, 'payment_schedule', total_amount / remaining_months)
    return loan.payment_schedule
def refresh(loan: Loan):
    calculate_amount(loan)   
    set_balance(loan)
    calculate_repayment_schedule(loan)
    return loan

def get_dict(loan: Loan):
    next_payment_date = loan.last_payment_date + relativedelta(months=1) if loan.last_payment_date else loan.application_date + relativedelta(months=1)
    number_of_days = (next_payment_date - datetime.now()).days

    return {'next_payment_date': next_payment_date, 'number_of_days': number_of_days, 'loan_type': loan.loan_type.type_name, 'date_borrowed': loan.application_date,
             'balance': loan.balance, 'total_amount': loan.total_amount, 'payment_schedule': loan.payment_schedule
            }