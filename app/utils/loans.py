# from fastapi import Depends
from sqlalchemy.orm import session

from sql.models_alchemy import Loan
from schemas.loans import loanCreate

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