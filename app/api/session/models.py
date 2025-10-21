from beanie import PydanticObjectId
from pydantic import BaseModel


class CreateData(BaseModel):
    session_id: PydanticObjectId


class CreateResponse(BaseModel):
    response: CreateData


class DeleteInput(BaseModel):
    session_id: PydanticObjectId
