from fastapi import APIRouter, status

from . import models, usecases

router = APIRouter(
    prefix='/session',
    tags=['Session']
)

@router.post('', response_model=models.CreateResponse)
async def create_session(body: models.CreateInput) -> models.CreateResponse:
    response = await usecases.create_session(user_id=body.user_id)
    return {}

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(body: models.DeleteInput) -> None:
    await usecases.delete_session(session_id=body.session_id)
    return