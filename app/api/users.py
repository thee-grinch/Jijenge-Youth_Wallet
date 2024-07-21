from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from sqlalchemy.sql import func

from sql.models_alchemy import User, Loan, Contribution, Saving, Notification, Share
from sql.database_alchemy import get_db, SessionLocal
from utils.utils import hash_pass, verify_password
from utils.user_verification import create_link, decode_token
from utils.send_mail import send_mail
from utils.user_methods import user_dict
import schemas.users
from utils.oauth import create_access_token, get_current_user
from schemas.schemas import *
from utils.totals import fetch_totals
from utils.notifications import get_notifications
from utils.transactions import get_transactions
from utils.loans import get_loan_types, get_dict
from input import add_user

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
    if not user:
        raise HTTPException(status_code=404, detail='User does not exist')
    try:
        if user.administrator.admin_id:
            return {'name': f"{user.first_name} {user.last_name}", 'admin': True}
    except:
        pass
    return {'name': f"{user.first_name} {user.last_name}"}

@router.get('/app/user')
def dashboard(user_id: int = Depends(get_current_user), db: session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    admin = False
    try:
        if user.administrator.admin_id:
            admin = True
    except:
        pass
    total_loans = db.query(func.sum(Loan.amount)).scalar()
    total_contributions = db.query(func.sum(Contribution.amount)).scalar()
    total_savings = db.query(func.sum(Saving.amount)).scalar()
    user_savings = db.query(func.sum(Saving.amount)).filter(Saving.user_id == user_id).scalar()
    user_loans = db.query(func.sum(Loan.amount)).filter(Loan.user_id == user_id).scalar()
    user_contributions = db.query(func.sum(Contribution.amount)).filter(Contribution.user_id == user_id).scalar()
    user_shares = db.query(func.sum(Share.amount)).filter(Share.user_id == user_id).scalar()
    notifications = get_notifications(db, user_id)
    transactions = get_transactions(db, user_id)
    totals =fetch_totals(db)
    user_response = {'name': f"{user.first_name} {user.last_name}", 'group': totals, 'user': {'savings': user_savings or 0, 'loans': user_loans or 0, 'contributions': user_contributions or 0, 'shares': user_shares or 0}, 'notifications': notifications, 'transactions': transactions}
    loantypes = get_loan_types(db)
    loan = db.query(Loan).filter(Loan.user_id == user_id).first()
    if loan:
        loan = get_dict(loan)
    else:
        loan = {}
    
    return {'user_response': user_response, 'loans': loan, 'loantypes': loantypes, 'admin': admin, 'notifications': notifications[:5], 'transactions': transactions[:5]}
    
    # return {'name': f"{user.first_name} {user.last_name}", 'group': totals, 'user': {'savings': user_savings or 0, 'loans': user_loans or 0, 'contributions': user_contributions or 0, 'shares': user_shares or 0}, 'notifications': notifications, 'transactions': transactions}

@router.get('/app/fake_user')
def add_fake_user(db: session = Depends(get_db)):
    for i in range(10):
        add_user(db)
    return {'message': 'fake users added successfully'}