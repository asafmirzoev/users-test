from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.schemas.pydantic.ClientSchema import (
    ClientPostRequestSchema
)
from app.services.ClientService import ClientService


ClientRouter = APIRouter(
    prefix="/v1/clients", tags=["client"]
)


@ClientRouter.post("/signup", status_code=status.HTTP_200_OK)
def signup(user: ClientPostRequestSchema, clientService: ClientService = Depends()):
    return clientService.sigup(user)


@ClientRouter.post("/signin", status_code=status.HTTP_200_OK)
def signin(user: ClientPostRequestSchema, clientService: ClientService = Depends()):
    return clientService.sigin(user)
