import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from ...shared.database.database import get_db
from ...shared.database.entities.user_account import UserAccount
from ...shared.exceptions.not_found import NotFoundError
from ...shared.exceptions.unauthorized import UnauthorizedError
from . import models

load_dotenv()

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def authenticate_user(db: Session, email: str, password: str) -> UserAccount|bool:
    user = db.query(UserAccount).filter(UserAccount.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

async def login(db: Session, email: str, password: str) -> models.LoginData:
    user = authenticate_user(db=db, email=email, password=password)
    if not user:
        raise NotFoundError(name='Usuário')
    
    access_token_expires = timedelta(minutes=int(os.getenv('TOKEN_EXPIRE_MINUTES')))
    access_token = create_token(data={'sub':str(user.pk_uuid)}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type':'bearer'}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        user_uuid = payload.get('sub')
        if user_uuid is None:
            raise UnauthorizedError()
    except InvalidTokenError:
        raise UnauthorizedError()
    user = db.query(UserAccount).filter(UserAccount.pk_uuid == user_uuid, UserAccount.deactivated_at == None).first()
    if user is None:
        raise NotFoundError(name='Usuário')
    return user