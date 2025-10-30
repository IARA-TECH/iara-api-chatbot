import os
from datetime import datetime, timedelta, timezone

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
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def authenticate_user(db: Session, email: str, password: str) -> UserAccount | bool:
    user = db.query(UserAccount).filter(UserAccount.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(
    data: dict, secret_key: str, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


async def login(db: Session, email: str, password: str) -> models.LoginData:
    user = authenticate_user(db=db, email=email, password=password)
    if not user:
        raise NotFoundError(name="Usuário")

    access_token_expires = timedelta(hours=int(os.getenv("ACCESS_TOKEN_EXPIRE")))
    access_token = create_token(
        data={"sub": str(user.pk_uuid)},
        expires_delta=access_token_expires,
        secret_key=os.getenv("ACCESS_SECRET_KEY"),
    )
    refresh_token_expires = timedelta(hours=int(os.getenv("REFRESH_TOKEN_EXPIRE")))
    refresh_token = create_token(
        data={"sub": str(user.pk_uuid), "password": password},
        expires_delta=refresh_token_expires,
        secret_key=os.getenv("REFRESH_SECRET_KEY"),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def refresh(db: Session, refresh_token: str) -> models.refreshData:
    payload = jwt.decode(
        refresh_token,
        os.getenv("REFRESH_SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")],
    )
    user_id = payload.get("sub")
    password = payload.get("password")
    if not user_id or not password:
        raise UnauthorizedError()

    user = (
        db.query(UserAccount)
        .filter(UserAccount.pk_uuid == user_id, UserAccount.password == password)
        .first()
    )
    if not user:
        raise UnauthorizedError()
    
    access_token_expires = timedelta(hours=int(os.getenv("ACCESS_TOKEN_EXPIRE")))
    access_token = create_token(
        data={"sub": str(user.pk_uuid)},
        expires_delta=access_token_expires,
        secret_key=os.getenv("ACCESS_SECRET_KEY"),
    )
    refresh_token_expires = timedelta(hours=int(os.getenv("REFRESH_TOKEN_EXPIRE")))
    refresh_token = create_token(
        data={"sub": str(user.pk_uuid), "password": user.password},
        expires_delta=refresh_token_expires,
        secret_key=os.getenv("REFRESH_SECRET_KEY"),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserAccount:
    try:
        payload = jwt.decode(
            token,
            os.getenv("ACCESS_SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
            options={"verify_exp": True},
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError()
    except InvalidTokenError:
        raise UnauthorizedError()
    user = (
        db.query(UserAccount)
        .filter(UserAccount.pk_uuid == user_id, UserAccount.deactivated_at == None)
        .first()
    )
    if user is None:
        raise NotFoundError(name="Usuário")
    return user
