from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import session

from schemas import loans, shares, contributions
from utils.oauth import get_current_user
from utils.loans import new_loan, new_loanType, pay_loan
from utils.shares import new_share
from utils.contributions import new_contribution
from sql.database_alchemy import get_db
from sql.models_alchemy import Loan, LoanType, Administrator
from utils.transactions import new_transaction
from utils.totals import find_total
from utils.notifications import new_notification

router = APIRouter()

@router.get('/app/get_loan_types')
def get_loantypes(db: session = Depends(get_db)):
    #function that get types
    loan_types = []
    source = db.query(LoanType).order_by(LoanType.loan_type_id).all()
    for type in source:
        loan_types.append(type.type_name)
    return loan_types

@router.post('/app/new_loan_type')
def create_loanType(new_type: loans.loanType, db: session = Depends(get_db), admin_id = Depends(get_current_user)):
    admin = db.query(Administrator).filter(Administrator.user_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail='You are not an admin')
    return new_loanType(new_type, db)

@router.post('/app/new_loan')
def create_loan(loan: loans.loanCreate, admin_id = Depends(get_current_user), db: session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.user_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail='You are not an admin')
    new_transaction(db, loan.user_id, 'loan', loan.amount)
    new_notification(db, loan.user_id, 'loan', loan.amount)
    find_total(db, loan.amount, 'loans')
    return new_loan(loan, db, loan.user_id)

@router.post('/app/pay_loan')
def repay(loan_data: loans.loan_pay, admin_id: int = Depends(get_current_user), db: session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.user_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail='You are not an admin')
    loan = db.query(Loan).filter(Loan.user_id == loan_data.user_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail='Loan does not exist')
    new_transaction(db, loan_data.user_id, 'loan Payment', loan_data.amount)
    new_notification(db, loan_data.user_id, 'payment', loan_data.amount)
    return pay_loan(loan, loan_data.amount, db)

@router.post('/app/add_shares')
def add_new_share(share: shares.shareCreate, admin_id: int = Depends(get_current_user),  db: session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.user_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail='You are not an admin')
    new_transaction(db, share.user_id, 'share', share.amount)
    new_notification(db, share.user_id, 'share', share.amount)
    return new_share(db, share.user_id, share.amount)

@router.post('/app/add_contribution')
def add_new_contribution(data: contributions.ContributionSchema, admin_id: int = Depends(get_current_user), db: session = Depends(get_db)):
    admin = db.query(Administrator).filter(Administrator.user_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=401, detail='You are not an admin')
    new_transaction(db, data.user_id, 'contribution', data.amount)
    new_notification(db, data.user_id, 'contribution', data.amount)
    return new_contribution(db, data.user_id, data.amount)
    


