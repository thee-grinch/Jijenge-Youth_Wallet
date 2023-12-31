from fastapi import FastAPI
from sqlmodel import Session
from datetime import datetime

from sql.database import create_db_and_tables, engine, yield_session
from sql.models import User, Contribution, Loan, LoanType, Administrator, Saving
# from sql.dbfunctions import create_user
app = FastAPI()

@app.on_event('startup')
def main():
    create_db_and_tables()

@app.post('/')
def create_user(new_user: User):
    """creates a new user to the database"""
    setattr(new_user, 'registration_date', datetime.fromisoformat(new_user.registration_date))
    setattr(new_user, 'last_login_date', datetime.fromisoformat(new_user.last_login_date))
    with yield_session() as session:
        session.add(new_user)
        try:
            session.commit()
        except Exception as e:
            return {'new user not created': e}
        session.refresh(new_user)
        return {'message': "{} was created successfully".format(new_user.first_name)}
