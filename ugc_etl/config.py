from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field("kafka", env="KAFKA_HOST")
    kafka_port: int = Field(9092, env="KAFKA_PORT")
    clickhouse_host: str = Field("clickhouse-node1", env="CLICKHOUSE_HOST")
    clickhouse_dbname: str = Field("cinema_analytics", env="CLICKHOUSE_DBNAME")
    kafka_topic: str = Field("view_progress", env="KAFKA_TOPIC")
    kafka_max_block_size: int = Field(1048576, env="KAFKA_MAX_BLOCK_SIZE")
    mongo_host: str = Field("mongodb", env="MONGO_HOST")
    mongo_port: int = Field(27017, env="MONGO_PORT")
    mongo_dbname: str = Field("ugc_movies", env="MONGO_DBNAME")
    mongo_collections: tuple = Field(('likes', 'bookmarks', 'reviews'))

    class Config:
        env_file = "envs/.env"


settings = Settings()
