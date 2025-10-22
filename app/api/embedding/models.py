from pydantic import BaseModel


class GetEmbeddingData(BaseModel):
    text: str
