from datetime import datetime
from typing import List, Optional
from uuid import UUID

from beanie import Document
from pydantic import BaseModel, Field


class Chat(BaseModel):
    user_message: str
    response: str
    agent_id: int
    sent_at: datetime


class Session(Document):
    user_id: UUID
    created_at: datetime
    chats: Optional[List[Chat]] = Field(default=None)
