"""
this module describes all the loans endpoints

"""
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import session

from utils.oauth import get_current_user
from sql.models import User
from sql.models_alchemy import Loan
from sql.database_alchemy import get_db
from schemas import loans
# from schemas.loans import Loan, loanCreate, loanType
from utils.loans import new_loan, new_loanType, calculate_amount, refresh, pay_loan
router = APIRouter()

@router.post('/app/new_loan')
def create_loan(loan: loans.loanCreate, user_id = Depends(get_current_user), db: session = Depends(get_db)):
    return new_loan(loan, user_id, db)

@router.get('/app/loan_status')
def get_status(user_id = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    calculate_amount(user.loans[0])
    return {'message': user.loans[0].total_amount}

@router.post('/app/new_loan_type')
def create_loanType(new_type: loans.loanType, db: session = Depends(get_db)):
    return new_loanType(new_type, db)

@router.get('/app/loans')
def get_loan(user_id = Depends(get_current_user), db: session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.user_id == user_id).first()
    
    if loan:
        my_return = {}
        keys = ['status', 'application_date', 'last_payment_date', 'balance']
        refresh(loan)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        for key, value in loan.__dict__.items():
            if key in keys:
                my_return[key] = value
        return my_return
    return {'message': 'No loans found'}

@router.post('/app/pay_loan')
def repay(amount_paid: loans.loan_pay, user_id = Depends(get_current_user), db: session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.user_id == user_id).first()
    if not loan:
        return {'message': 'user has no loans'}
    return pay_loan(loan, amount_paid.amount)
