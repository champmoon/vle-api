from __future__ import annotations

from pydantic import BaseSettings, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: str
    PROTOCOL: str = "http"

    SERVER_HOSTNAME: str | None = None

    @validator("SERVER_HOSTNAME", pre=True)
    def assemble_server_(cls, v: str | None, values: dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return HttpUrl.build(
            scheme=values["PROTOCOL"],
            host=values["SERVER_HOST"],
            port=values["SERVER_PORT"],
        )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("ASYNC_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST") or "",
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SUPER_USER_USERNAME: str
    SUPER_USER_PASSWORD: str
    SUPER_USER_EMAIL: str

    STATIC_FILES_DIR: str

    @classmethod
    def from_env(cls) -> Settings:
        return cls.parse_obj({})

    class Config:
        case_sensitive = True


settings = Settings.from_env()
