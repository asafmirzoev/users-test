import datetime

from sqlalchemy import (
    Column, Integer, PrimaryKeyConstraint, String, Text
)
from app.models.BaseModel import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer)
    username = Column(String(16), nullable=False, unique=True)
    password = Column(Text)

    PrimaryKeyConstraint(id)
