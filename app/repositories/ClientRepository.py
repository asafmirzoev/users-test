from typing import Sequence, Optional
from argon2 import PasswordHasher

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row

from app.core.Database import get_db_connection
from app.core.Exceptions import NotFoundError, AlreadyExistsError
from app.auth.auth_handler import signJWT, decodeJWT
from app.models.ClientModel import Client


def generate_pwd_hash(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


def check_pwd_hash(hash: str, password: str) -> str:
    ph = PasswordHasher()
    return ph.verify(hash, password)


class ClientRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def get_client(self, username: str) -> Row | None:
        query_string = text(f"SELECT * FROM clients WHERE clients.username=:username")
        return self.db.execute(query_string, {'username': username.lower()}).fetchone()

    def signup(self, username: str, password: str) -> dict:
        if self.get_client(username): raise AlreadyExistsError(detail=f"Client with username \"{username}\" already exists")
        
        query_string = text("INSERT INTO clients (username, password) VALUES (:usrnm, :pwd) RETURNING id")
        user_id = self.db.execute(query_string, {'usrnm': username, 'pwd': generate_pwd_hash(password)}).scalar()
        self.db.commit()

        return signJWT(user_id)
    
    def signin(self, username: str, password: str) -> dict:
        if not (client := self.get_client(username)): raise NotFoundError(detail=f"Client not found")
        if check_pwd_hash(client[2], password): return signJWT(client[0])

