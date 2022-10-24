import os

from pydantic import BaseSettings


RUN_LEVEL = os.getenv("RUN_LEVEL", "dev")


class ToolConfig:
    env_file_encoding = "utf8"
    extra = "ignore"


class AppSettings(BaseSettings):
    PORT: int = 8080

    class Config(ToolConfig):
        env_prefix = "app_"
