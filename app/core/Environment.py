import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    
    API_VERSION: str
    APP_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    DEBUG_MODE: bool

    model_config = SettingsConfigDict(env_file=get_env_filename(), env_file_encoding='utf-8')


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
