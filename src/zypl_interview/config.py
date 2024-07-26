import datetime
from datetime import tzinfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_DRIVER: str
    DB_USERNAME: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_ECHO: bool
    JWT_SECRET: str
    JWT_ALGORITHM: str

    TIME_ZONE: tzinfo = datetime.UTC


config = Config()
