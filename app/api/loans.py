"""
this module describes all the loans endpoints

"""
from fastapi import Depends, APIRouter
from sqlalchemy.orm import session

from utils.oauth import get_current_user
from sql.models import User
from sql.database_alchemy import get_db
from schemas.loans import Loan, loanCreate
from utils.loans import new_loan
router = APIRouter()

@router.post('/new_loan')
def create_loan(loan: loanCreate, user_id = Depends(get_current_user), db: session = Depends(get_db)):
    return new_loan(loan, user_id, db)

@router.get('/loan_status')
def get_status(user_id = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {'message': user.loans[0].status}

