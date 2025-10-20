from datetime import datetime
from uuid import UUID
from bson import ObjectId

from ...shared.database.entities.session import Session
from ...shared.exceptions.not_found import NotFoundError
from . import models

async def create_session(user_id: UUID) -> models.CreateData:
    session = Session(user_id=user_id, created_at=datetime.now())
    await Session.insert_one(session)
    return {'session_id': str(session.id)}

async def delete_session(session_id: ObjectId, user_id: UUID) -> None:
    session = await Session.find_one(Session.id==session_id)
    if (not session):
        raise NotFoundError(name='Sessão', id=session_id)
    if (session.user_id != user_id):
        raise NotFoundError(name='Sessão', id=session_id)
    else: 
        await session.delete()
    return 