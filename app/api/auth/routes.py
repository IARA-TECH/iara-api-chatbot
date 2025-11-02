from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...shared.database.database import get_db
from ...shared.database.entities.user_account import UserAccount
from . import models, usecases

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=models.LoginResponse)
async def login(
    body: models.LoginInput, db: Session = Depends(get_db)
) -> models.LoginResponse:
    response = await usecases.login(db=db, email=body.email, password=body.password)
    return {"response": response}


@router.post("/refresh", response_model=models.refreshResponse)
async def refresh(
    body: models.refreshInput, db: Session = Depends(get_db)
) -> models.refreshResponse:
    response = await usecases.refresh(db=db, refresh_token=body.refresh_token)
    return {"response": response}
