from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field("kafka", env="KAFKA_HOST")
    kafka_port: int = Field(9092, env="KAFKA_PORT")
    clickhouse_host: str = Field("clickhouse-node1", env="CLICKHOUSE_HOST")
    kafka_topic: str = Field("view_progress", env="KAFKA_TOPIC")
    kafka_max_block_size: int = Field(1048576, env="KAFKA_MAX_BLOCK_SIZE")

    class Config:
        env_file = "envs/.env"


settings = Settings()
