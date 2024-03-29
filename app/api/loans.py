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
from utils.transactions import new_transaction
from utils.notifications import new_notification
# from schemas.loans import Loan, loanCreate, loanType
from utils.loans import new_loan, new_loanType, calculate_amount, refresh, pay_loan, get_dict
router = APIRouter()

# @router.post('/app/new_loan')
# def create_loan(loan: loans.loanCreate, user_id = Depends(get_current_user), db: session = Depends(get_db)):
#     new_transaction(db, user_id, 'loan', loan.amount)
#     return new_loan(loan, user_id, db)

@router.get('/app/loan_status')
def get_status(user_id = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    calculate_amount(user.loans[0])
    return {'message': user.loans[0].total_amount}



@router.get('/app/loans')
def get_loan(user_id = Depends(get_current_user), db: session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.user_id == user_id).first()
    
    if loan:
        my_return = {}
        # keys = ['status', 'application_date', 'last_payment_date', 'balance', 'loan_type']
        refresh(loan)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return get_dict(loan)
    return {'message': 'No loans found'}

# @router.post('/app/pay_loan')
# def repay(amount_paid: loans.loan_pay, user_id = Depends(get_current_user), db: session = Depends(get_db)):
#     new_notification(db, user_id, 'loan Payment', amount_paid.amount)
#     new_transaction(db, user_id, 'loan Payment', amount_paid.amount)
#     loan = db.query(Loan).filter(Loan.user_id == user_id).first()
#     if not loan:
#         return {'message': 'user has no loans'}
#     new_transaction(db, user_id, 'loan Payment', amount_paid.amount)
#     return pay_loan(loan, amount_paid.amount)
