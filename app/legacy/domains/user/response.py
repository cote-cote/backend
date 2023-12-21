from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    user_name: str
    user_email: str


class Token(BaseModel):
    value: str
