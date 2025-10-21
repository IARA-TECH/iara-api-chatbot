from pydantic import BaseModel


class LoginInput(BaseModel):
    email: str
    password: str


class LoginData(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    response: LoginData
