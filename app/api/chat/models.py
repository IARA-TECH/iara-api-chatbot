from beanie import BeanieObjectId
from pydantic import BaseModel


class RespondInput(BaseModel):
    session_id: BeanieObjectId
    user_message: str


class RespondData(BaseModel):
    response: str


class RespondResponse(BaseModel):
    response: RespondData
