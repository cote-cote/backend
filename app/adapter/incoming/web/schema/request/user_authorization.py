from pydantic import BaseModel


class UserAuthorization(BaseModel):
    auth_code: str
