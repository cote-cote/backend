from pydantic import BaseModel


class Token(BaseModel):
    value: str


class RequestUserAuthorization(BaseModel):
    auth_code: str
