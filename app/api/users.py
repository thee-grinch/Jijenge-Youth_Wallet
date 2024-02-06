from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from sql.models import User
from sql.database import get_db
from utils.utils import hash_pass, verify_password
from utils.user_verification import create_link, decode_token
from utils.send_mail import send_mail
from schemas.user import *
from utils.oauth import create_access_token
from schemas.schemas import *

router = APIRouter()

@router.post('/new/')
def create_user(new_user: CreateUser, db: Session = Depends(get_db)):
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

@router.get('/verify')
def verify_user(token: str, db: Session = Depends(get_db)):
    email = decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)

@router.post('/login', response_model=Token)
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == userdetails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The user Does Not Exist")
    if not verify_password(userdetails.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"The passwords do not match")
    access_token = create_access_token(data={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}