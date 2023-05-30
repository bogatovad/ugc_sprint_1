from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field("ugc", env="PROJECT_NAME")
    host: str = Field("ugc_api_2", env="UGC_2_HOST")
    port: int = Field(8080, env="UGC_2_PORT")
    mongo_host: str = Field("mongodb", env="MONGO_HOST")
    mongo_port: int = Field(27017, env="MONGO_PORT")
    mongo_dbname: str = Field("ugc_movies", env="MONGO_DBNAME")
    
    class Config:
        env_file = "envs/.env"


settings = Settings()
