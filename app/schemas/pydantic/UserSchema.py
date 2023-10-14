import datetime
from pydantic import BaseModel


class UserPostRequestSchema(BaseModel):
    name: str


class UserSchema(BaseModel):
    id: int
    name: str
    first_login: datetime.datetime
