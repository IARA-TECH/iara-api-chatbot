from datetime import datetime
from uuid import UUID

from ...shared.database.entities.session import Chat, Session
from ...shared.exceptions.not_found import NotFoundError
from ..agents.usecases import create_response
from . import models


async def get_history(session_id: UUID) -> list | bool:
    session = await Session.find_one(Session.id == session_id)
    if not session:
        return False

    if session.chats:
        history = session.chats[-6:]
        history = [
            (role, message)
            for chat in history
            for role, message in [("human", chat.user_message), ("ai", chat.response)]
        ]
    else:
        history = []
    return history


async def respond(
    session_id: UUID, user_message: str, user_id: UUID
) -> models.RespondData:
    session = await Session.find_one(Session.id == session_id)
    if not session:
        raise NotFoundError(name="Sessão")
    if session.user_id != user_id:
        raise NotFoundError(name="Sessão")

    history = await get_history(session_id=session_id)
    result = create_response(user_message=user_message, history=history)

    response = result["response"]
    agent_id = result["agent_id"]

    chat = Chat(
        user_message=user_message,
        response=response,
        agent_id=agent_id,
        sent_at=datetime.now(),
    )

    if session.chats:
        session.chats.append(chat)
    else:
        session.chats = [chat]

    await session.save()

    return {"response": response}
