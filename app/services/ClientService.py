from fastapi import Depends

from sqlalchemy.engine.row import Row

from app.repositories.ClientRepository import ClientRepository
from app.schemas.pydantic.ClientSchema import ClientSchema


class ClientService:
    clientRepository: ClientRepository

    def __init__(self, clientRepository: ClientRepository = Depends()) -> None:
        self.clientRepository = clientRepository

    def sigup(self, client_body: ClientSchema) -> Row:
        token = self.clientRepository.signup(username=client_body.username, password=client_body.password)
        return token
    
    def sigin(self, client_body: ClientSchema) -> Row:
        if (token := self.clientRepository.signin(username=client_body.username, password=client_body.password)):
            return token
        return {"error": "Wrong login details!"}
