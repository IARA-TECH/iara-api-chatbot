from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, Field


class Chat(BaseModel):
    user_message: str
    response: str
    agent_id: int
    sent_at: datetime
    total_tokens: int

class Session(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id") 
    user_id: UUID
    created_at: datetime
    chats: Optional[List[Chat]] = Field(default=None)