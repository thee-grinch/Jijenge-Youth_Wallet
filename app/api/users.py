from fastapi import APIRouter, Depends
from sqlmodel import Session

from sql.models import User
from sql.database import get_db
from utils.utils import hash_pass
from utils.user_verification import create_link
from utils.send_mail import send_mail
from schemas.user import *

router = APIRouter()

@router.post('/new/')
def create_user(new_user: CreateUser, db: Session = Depends(get_db)):
    """creates a new user to the database
        this route is responsible for creating a new user,
        Arguments:
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