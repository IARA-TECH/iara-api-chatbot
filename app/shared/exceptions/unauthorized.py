from fastapi import HTTPException


class UnauthorizedError(HTTPException):
    def __init__(self):
        message = f"Usuário sem acesso"
        super().__init__(status_code=401, detail=message)
