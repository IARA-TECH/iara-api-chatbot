from fastapi import HTTPException


class BadRequestError(HTTPException):
    def __init__(self, message: str = None):
        message = f"Requisição inválida {message}" if message else "Requisição inválida"
        super().__init__(status_code=400, detail=message)
