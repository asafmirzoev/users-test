import datetime
from pydantic import BaseModel


class ClientPostRequestSchema(BaseModel):
    username: str
    password: str


class ClientSchema(ClientPostRequestSchema):
    pass
