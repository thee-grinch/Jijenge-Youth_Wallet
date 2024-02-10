from datetime import datetime
from math import ceil
from dateutil.relativedelta import relativedelta

from sql.models import User, Loan, LoanType

def approve_loan(loan: Loan):
    """this function helps the administrator approve a loan"""
    loan.status = "approved"

# def calculate_amount(loan: Loan, type: LoanType):
#     """this calculates the total loan amount with simple interest"""
#     loan_borrowed = loan.amount
#     current_amount = loan.total_amount
#     interest_rate = type.interest_rate
#     last_payment_date = loan.last_payment_date if  loan.last_payment_date else loan.application_date
#     interest = ceil((loan_borrowed / 100) * interest_rate)
#     if (datetime.now() - last_payment_date).days > 30:
#         current_amount += interest
#     return current_amount


def calculate_amount(loan: Loan, type: LoanType):
    loan_borrowed = loan.amount
    current_amount = loan.total_amount or loan_borrowed
    interest_rate = type.interest_rate / 100
    repayment_period = type.repayment_period
    last_payment_date = loan.last_payment_date if loan.last_payment_date else loan.application_date
    months_since_borrowed = relativedelta(datetime.now(), last_payment_date).months
    monthly_interest = loan_borrowed * interest_rate / repayment_period
    interest = monthly_interest * months_since_borrowed
    print(months_since_borrowed)
    current_amount += interest
    return months_since_borrowed

def calculate_balance(loan: Loan):
    """ calculates the loan balance"""
    loan.balance = loan.total_paid - loan.total_amount

def calculate_payment_schedule(loan: Loan, type: LoanType):
    """calculates the loan schedule"""
    loan_borrowed = loan.amount
    interest_rate = type.interest_rate
    time = type.repayment_period
    months_repayed = (datetime.utcnow() - loan.application_date).days // 30
    total_paid = loan.total_paid
    total_amount = loan.total_amount
    total_to_be_paid = loan_borrowed / 100 * interest_rate * time
    total_loan = total_to_be_paid if total_to_be_paid > total_amount else total_amount
    remaining_time = abs(time - months_repayed)
    loan.payment_schedule = (total_loan)  / remaining_time

    