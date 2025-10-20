from pydantic import BaseModel

from beanie import PydanticObjectId

class CreateData(BaseModel):
    session_id: PydanticObjectId

class CreateResponse(BaseModel):
    response: CreateData

class DeleteInput(BaseModel):
    session_id: PydanticObjectId