from fastapi import HTTPException

class NotFoundError(HTTPException):
    def __init__(self, name: str, id: any = None):
        message = f"{name} não encontrado(a)" if id is None else f"{name} com id {id} não encontrado(a)"
        super().__init__(status_code=404, detail=message)