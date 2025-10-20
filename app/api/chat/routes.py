from fastapi import APIRouter, Depends

from . import models, usecases
from ...shared.database.entities.user_account import UserAccount
from ..auth.usecases import get_current_user

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

@router.post('/', response_model=models.RespondResponse)
async def create_session(
    body: models.RespondInput,
    current_user: UserAccount = Depends(get_current_user)
) -> models.RespondResponse:
    response = await usecases.respond(body.session_id, body.user_message, current_user.pk_uuid)
    return {'response': response}