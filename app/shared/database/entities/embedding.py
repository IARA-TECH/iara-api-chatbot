from beanie import Document


class Embedding(Document):
    document_name: str
    part: int
    text: str
    embedding: list
