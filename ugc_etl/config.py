from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field('kafka', env='KAFKA_HOST')
    kafka_port: int = Field(9092, env='KAFKA_PORT')
    clickhouse_host: str = Field('clickhouse-node1', env='CLICKHOUSE_HOST')
    topic_list: str = Field('view_progress', env='topic_list')

    class Config:
        env_file = "envs/.env"


settings = Settings()
