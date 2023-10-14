from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.auth.auth_bearer import JWTBearer
from app.schemas.pydantic.UserSchema import (
    UserPostRequestSchema, UserSchema
)
from app.services.UserService import UserService


UserRouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)


@UserRouter.get("/", dependencies=[Depends(JWTBearer())], response_model=List[UserSchema])
def index(
    name: Optional[str] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    userService: UserService = Depends()
):
    return userService.list(name, order_by, limit, offset)


@UserRouter.get("/{id}", dependencies=[Depends(JWTBearer())], response_model=UserSchema)
def get(id: int, userService: UserService = Depends()):
    return userService.get(id)


@UserRouter.post("/", dependencies=[Depends(JWTBearer())], response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create(user: UserPostRequestSchema, userService: UserService = Depends()):
    return userService.create(user)


@UserRouter.patch("/{id}", dependencies=[Depends(JWTBearer())], response_model=UserSchema)
def update(id: int, user: UserPostRequestSchema, userService: UserService = Depends()):
    return userService.update(id, user)


@UserRouter.delete("/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, userService: UserService = Depends()):
    return userService.delete(id)