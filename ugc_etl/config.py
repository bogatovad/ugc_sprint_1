#from dotenv import load_dotenv

from pydantic import BaseSettings, Field


#load_dotenv()

class Settings(BaseSettings):
    kafka_host: str = Field('kafka', env='KAFKA_HOST')
    kafka_port: int = Field(9092, env='KAFKA_PORT')
    clickhouse_host: str = Field('0.0.0.0', env='CLICKHOUSE_HOST') 

    class Config:
        env_file = ".env"


settings = Settings()

