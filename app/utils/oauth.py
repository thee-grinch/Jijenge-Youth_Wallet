from datetime import timedelta, datetime
import time

from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlmodel import Session

from sql import models
from sql import database
from schemas import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
SECRET_KEY = "d009f93e6b8eb75a1057a5a4ab8a092d91b44de7ce42e6a9d388abe1739c3cca"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_timestamp = int(time.time()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)  # Convert minutes to seconds
    to_encode.update({"exp": expire_timestamp})
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": int(time.mktime(expire.timetuple()))})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_token(authorization: Optional[str] = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Check if the Authorization header starts with "Bearer " and extract the token
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    token = authorization[len(prefix):]
    return token

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.DataToken(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(get_token), db: Session = Depends(database.get_db)):
    credendtials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate Credentials",
                                           headers={"WWW-Authenticate": "Bearer"})
    token = verify_token_access(token, credendtials_exception)
    # user = db.query(models.User).filter(models.User.id == token.id).first()
    return token.id

