from typing import Sequence, Optional

from fastapi import Depends

from sqlalchemy.engine.row import Row

from app.repositories.UserRepository import UserRepository
from app.schemas.pydantic.UserSchema import UserSchema


class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends()) -> None:
        self.userRepository = userRepository

    def create(self, user_body: UserSchema) -> Row:
        return self.userRepository.create(name=user_body.name)

    def delete(self, user_id: int) -> None:
        return self.userRepository.delete(user_id=user_id)

    def get(self, user_id: int) -> Row:
        return self.userRepository.get(user_id=user_id)

    def list(self, name: Optional[str], order_by: Optional[str], limit: Optional[int] = 100, offset: Optional[int] = 0) -> Sequence[Row]:
        return self.userRepository.list(name, order_by, limit, offset)

    def update(self, user_id: int, user_body: UserSchema) -> Row:
        return self.userRepository.update(user_id=user_id, name=user_body.name)
