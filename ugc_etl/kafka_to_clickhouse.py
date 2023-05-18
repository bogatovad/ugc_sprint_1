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
        "CREATE DATABASE IF NOT EXISTS cinema_analytics ON CLUSTER company_cluster",
    )


def create_ch_table(client):
    client.execute(
        """CREATE TABLE IF NOT EXISTS cinema_analytics.movie_views ON CLUSTER company_cluster(
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
        f"""CREATE TABLE IF NOT EXISTS cinema_analytics.kafka_movie_views(
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
        """CREATE MATERIALIZED VIEW IF NOT EXISTS cinema_analytics.mv_kafka_movie_views TO cinema_analytics.movie_views AS
            SELECT * FROM cinema_analytics.kafka_movie_views;"""
    )


def migrator():
    """Осущетсвляет интеграцию Kafka и Clickhouse"""
    ch_client = init_ch_connection()
    init_clickhouse_db(ch_client)
    create_ch_table(ch_client)
    logging.info('created Clickhouse analytics table')
    create_kafka_queue(ch_client)
    logging.info('created kafka queue table')
    create_ch_mv(ch_client)
    logging.info('created materialized view')


if __name__ == '__main__':
    migrator()
