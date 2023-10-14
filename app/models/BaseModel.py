from sqlalchemy.orm import declarative_base

from app.core.Database import Engine

# Base Model Schema
Base = declarative_base()


def init():
    Base.metadata.create_all(bind=Engine)
