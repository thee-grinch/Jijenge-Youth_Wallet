from fastapi import FastAPI, Depends,  HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session
from datetime import datetime

from utils.oauth import create_access_token
from sql.database import create_db_and_tables, engine, get_db
from sql.models import User, Contribution, Loan, LoanType, Administrator, Saving
from utils.utils import hash_pass, verify_password
from utils.user_verification import create_link, decode_token
from utils.send_mail import send_mail
from api import schemas
# from sql.dbfunctions import create_user
routers = APIRouter(
    tags=['Authentication']
)

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def main():
    create_db_and_tables()

@app.post('/new')
def create_user(new_user: User, db: Session = Depends(get_db)):
    """creates a new user to the database"""
    # setattr(new_user, 'registration_date', datetime.fromisoformat(new_user.registration_date))
    # setattr(new_user, 'last_login_date', datetime.fromisoformat(new_user.last_login_date))
    hashed_pass = hash_pass(new_user.password)
    new_user.password = hashed_pass
    # with Session(engine) as session:
    #     session.add(new_user)
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         return {'new user not created': e}
    #     session.refresh(new_user)
    #     return  {'message': "{} was created successfully".format(new_user.first_name)}
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user.name)
    link = create_link(new_user.email)
    send_mail(new_user.email, link, new_user.first_name)
    return {'message': "{} was created successfully".format(new_user.first_name)}
@app.get('/verify')
def verify_user(token: str, db: Session = Depends(get_db)):
    email = decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'email verified successfully'}
@app.post('/login', response_model=schemas.Token)
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == userdetails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The user Does Not Exist")
    if not verify_password(userdetails.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The passwords do not match")
    access_token = create_access_token(data={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
@app.post('loan')
def create_loan(new_loan: Loan):
    pass