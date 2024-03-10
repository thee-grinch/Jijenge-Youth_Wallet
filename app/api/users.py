from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from sqlalchemy.sql import func

from sql.models_alchemy import User, Loan, Contribution, Saving, Notification
from sql.database_alchemy import get_db, SessionLocal
from utils.utils import hash_pass, verify_password
from utils.user_verification import create_link, decode_token
from utils.send_mail import send_mail
from utils.user_methods import user_dict
import schemas.users
from utils.oauth import create_access_token, get_current_user
from schemas.schemas import *

router = APIRouter()

@router.post('/app/new/')
def create_user(new_user: schemas.users.createUser , db: session = Depends(get_db)):
    """
        creates a new user to the database
        Parameters:
            new_user: an instance of createUser class a schema with the necessary fields
            db: the session class, which represents the database which the user will be saved
        functioning:
            first the password is hashed
            the function initialises a mapped class of user with the details from the new user
            the user is added to the database
            a link is created 
            then the link is sent to the users email
    """
    hashed_pass = hash_pass(new_user.password)
    new_user.password = hashed_pass
    user = User(**new_user.__dict__)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(user.name)
    link = create_link(new_user.email)
    send_mail(new_user.email, link, new_user.first_name)
    return {'message': "{} was created successfully".format(new_user.first_name)}

@router.get('/app/verify')
def verify_user(token: str, db: session = Depends(get_db)):
    email = decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'user email was verified'}

@router.post('/app/login', response_model=Token)
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    user = db.query(User).filter(User.name == userdetails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The user Does Not Exist")
    if not verify_password(userdetails.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The passwords do not match")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/app/username')
def get_user(user_id: int = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return {'name': f"{user.first_name} {user.last_name}"}

@router.get('/app/user')
def dashboard(user_id: int = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    total_loans = db.query(func.sum(Loan.amount)).scalar()
    total_contributions = db.query(func.sum(Contribution.amount)).scalar()
    total_savings = db.query(func.sum(Saving.amount)).scalar()
    user_savings = db.query(func.sum(Saving.amount)).filter(Saving.user_id == user_id).scalar()
    user_loans = db.query(func.sum(Loan.amount)).filter(Loan.user_id == user_id).scalar()
    user_contributions = db.query(func.sum(Contribution.amount)).filter(Contribution.user_id == user_id).scalar()
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    return {'name': f"{user.first_name} {user.last_name}", 'group': {'savings': total_savings or 0, 'loans': total_loans or 0, 'contributions': total_contributions or 0}, 'user': {'savings': user_savings or 0, 'loans': user_loans or 0, 'contributions': user_contributions or 0}, 'notifications': notifications}
