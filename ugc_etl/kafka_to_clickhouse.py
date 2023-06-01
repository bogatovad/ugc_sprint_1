import logging

import backoff
from clickhouse_driver import Client
from config import settings

logging.basicConfig(level=logging.INFO)


@backoff.on_exception(
    backoff.expo,
    ConnectionError,
    max_tries=20,
)
def init_ch_connection():
    return Client(host=settings.clickhouse_host)


def init_clickhouse_db(client):
    client.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.clickhouse_dbname}",
    )


def create_ch_table(client):
    client.execute(
        f"""CREATE TABLE IF NOT EXISTS {settings.clickhouse_dbname}.movie_views(
        user_id String,
        movie_id String,
        movie_timestamp Int64,
        type String,
        created_at Datetime
        )
        Engine=MergeTree()
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at"""
    )


def create_kafka_queue(client):
    client.execute(
        f"""CREATE TABLE IF NOT EXISTS {settings.clickhouse_dbname}.kafka_movie_views(
            user_id String,
            movie_id String,
            movie_timestamp Int64,
            type String,
            created_at Datetime
            )
            ENGINE = Kafka
            SETTINGS
            kafka_broker_list = '{settings.kafka_host}:{settings.kafka_port}',
            kafka_topic_list = '{settings.kafka_topic}',
            kafka_group_name = 'clickhouse_reader',
            kafka_format = 'JSONEachRow',
            kafka_num_consumers = 1,
            kafka_max_block_size = {settings.kafka_max_block_size};"""
    )


def create_ch_mv(client):
    client.execute(
        f"""CREATE MATERIALIZED VIEW IF NOT EXISTS {settings.clickhouse_dbname}.mv_kafka_movie_views
        TO {settings.clickhouse_dbname}.movie_views AS
        SELECT * FROM {settings.clickhouse_dbname}.kafka_movie_views;"""
    )


def kafka_migrator():
    """Осущетсвляет интеграцию Kafka и Clickhouse"""
    ch_client = init_ch_connection()
    init_clickhouse_db(ch_client)
    create_ch_table(ch_client)
    logging.info("created Clickhouse analytics table")
    create_kafka_queue(ch_client)
    logging.info("created kafka queue table")
    create_ch_mv(ch_client)
    logging.info("created materialized view")


if __name__ == "__main__":
    kafka_migrator()
