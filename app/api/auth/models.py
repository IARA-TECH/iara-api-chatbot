from pydantic import BaseModel


class LoginInput(BaseModel):
    email: str
    password: str


class LoginData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginResponse(BaseModel):
    response: LoginData


class refreshInput(BaseModel):
    refresh_token: str


class refreshData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class refreshResponse(BaseModel):
    response: refreshData
