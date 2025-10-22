from pydantic import BaseModel


class CreateResponseData(BaseModel):
    response: str
    agent_id: int
