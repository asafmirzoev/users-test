import datetime
from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row

from app.core.Database import get_db_connection
from app.core.Exceptions import NotFoundError, AlreadyExistsError
from app.models.UserModel import User


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def get_user(self, user_id: int | None = None, user_name: str | None = None):
        query_string = text(f"SELECT users.id AS id, users.name AS name, users.first_login as first_login FROM users WHERE {'LOWER(users.name) LIKE :user_name' if user_name else 'users.id=:user_id'}")
        params = {'user_name': user_name} if user_name else {'user_id': user_id}
        return self.db.execute(query_string, params).fetchone()

    def list(self, name: Optional[str], order_by: Optional[str], limit: Optional[int], offset: Optional[int]) -> Sequence[Row]:
        order_by = f"ORDER BY {order_by} {'ASC' if order_by[0] == '-' else 'DESC'}" if order_by and hasattr(User, order_by.replace('-', '')) else ''
        
        query_string = text(f"SELECT users.id AS id, users.name AS name, users.first_login as first_login FROM users {'WHERE LOWER(users.name) LIKE :user_name' if name else ''} {order_by} LIMIT :limit OFFSET :offset")
        params = {
            'limit': limit,
            'offset': offset
        }
        if name: params.update({'user_name': name})

        query = self.db.execute(query_string, params).fetchall()
        return query

    def get(self, user_id: int) -> Row:
        if not (query := self.get_user(user_id=user_id)): raise NotFoundError(detail=f"User not found")
        return query

    def create(self, name: str) -> Row:

        if self.get_user(user_name=name): raise AlreadyExistsError(detail=f"User with name \"{name}\" already exists")

        query_string = text("INSERT INTO users (name, first_login) VALUES (:user_name, :user_first_login) RETURNING id")
        user_id = self.db.execute(query_string, {'user_name': name, 'user_first_login': datetime.datetime.now()}).scalar()
        self.db.commit()

        return self.get_user(user_id)

    def update(self, user_id: int, name: str) -> Row:
        if not self.get_user(user_id=user_id): raise NotFoundError(detail=f"User not found")

        query_string = text("UPDATE users SET name=:user_name WHERE users.id=:user_id")
        self.db.execute(query_string, {'user_name': name, 'user_id': user_id})
        self.db.commit()

        return self.get_user(user_id)

    def delete(self, user_id: int) -> None:
        if not self.get_user(user_id=user_id): raise NotFoundError(detail=f"User not found")

        query_string = text("DELETE FROM users WHERE users.id=:user_id")
        self.db.execute(query_string, {'user_id': user_id})
        self.db.commit()
