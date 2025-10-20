from fastapi import APIRouter, status, Depends

from . import models, usecases
from ...shared.database.entities.user_account import UserAccount
from ...api.auth.usecases import get_current_user

router = APIRouter(
    prefix='/session',
    tags=['Session']
)

@router.post('', response_model=models.CreateResponse)
async def create_session(
    current_user: UserAccount = Depends(get_current_user)
) -> models.CreateResponse:
    response = await usecases.create_session(current_user.pk_uuid)
    return {'response': response}

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    body: models.DeleteInput,
    current_user: UserAccount = Depends(get_current_user)
) -> None:
    await usecases.delete_session(session_id=body.session_id, user_id=current_user.pk_uuid)
    return