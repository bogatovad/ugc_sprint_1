import logging
from logging import config as logging_config

import logstash
from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


logger = logging.getLogger(__name__)
logstash_handler = logstash.LogstashHandler("logstash", 5044, version=1)
logger.addHandler(logstash_handler)


class Settings(BaseSettings):
    project_name: str = Field("ugc", env="PROJECT_NAME")
    host: str = Field("ugc_api_2", env="UGC_2_HOST")
    port: int = Field(8080, env="UGC_2_PORT")
    mongo_host: str = Field("mongodb", env="MONGO_HOST")
    mongo_port: int = Field(27017, env="MONGO_PORT")
    mongo_dbname: str = Field("ugc_movies", env="MONGO_DBNAME")
    authjwt_secret_key: str = Field("super-secret", env="JWT_SECRET_KEY")

    class Config:
        env_file = "envs/.env"


settings = Settings()
