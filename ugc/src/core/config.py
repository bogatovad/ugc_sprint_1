from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field('ugc', env='PROJECT_NAME')
    host: str = Field("ugc_api", env="UGC_HOST")
    port: int = Field(8000, env="UGC_PORT")
    kafka_host: str = Field('kafka', env="KAFKA_HOST")
    kafka_port: int = Field(9092, env="KAFRA_PORT")
    kafka_topic: str = Field('view_progress', env="KAFKA_TOPIC")

    class Config:
        env_file = "envs/.env"


settings = Settings()
