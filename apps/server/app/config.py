from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_port: int = Field(default=8080, alias="API_PORT")

    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5433/swipetune",
        alias="DATABASE_URL",
    )

    s3_endpoint: str | None = Field(default="http://localhost:9000", alias="S3_ENDPOINT")
    s3_bucket: str = Field(default="swipetune-tracks", alias="S3_BUCKET")
    s3_access_key: str = Field(default="localkey", alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(default="localsecret", alias="S3_SECRET_KEY")
    s3_region: str | None = Field(default="ap-northeast-1", alias="S3_REGION")

    music_gen_api_base: str | None = Field(default=None, alias="MUSIC_GEN_API_BASE")
    music_gen_api_key: str | None = Field(default=None, alias="MUSIC_GEN_API_KEY")

    allowed_origins: str = Field(default="http://localhost:8081", alias="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()

