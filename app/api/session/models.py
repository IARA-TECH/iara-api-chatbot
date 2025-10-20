from uuid import UUID

from pydantic import BaseModel

class CreateInput(BaseModel):
    user_id: UUID

class CreateResponse(BaseModel):
    session_id: UUID

class DeleteInput(BaseModel):
    session_id: UUID