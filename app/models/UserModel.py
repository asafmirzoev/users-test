import datetime

from sqlalchemy import (
    Column, Integer, PrimaryKeyConstraint, String, DateTime
)
from app.models.BaseModel import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer)
    name = Column(String(64), nullable=False, index=True)
    first_login = Column(DateTime, nullable=False, default=datetime.datetime.now)

    PrimaryKeyConstraint(id)
