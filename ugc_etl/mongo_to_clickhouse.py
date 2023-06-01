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
        f"""CREATE TABLE IF NOT EXISTS {settings.clickhouse_dbname}.ratings(
        user_id String,
        movie_id String,
        rating Int32
        )
        Engine=MongoDB(
        '{settings.mongo_host}:{settings.mongo_port}',
        '{settings.mongo_dbname}',
        'likes', '', '');"""
    )


def mongo_migrator():
    """Осущетсвляет интеграцию MongoDB и Clickhouse"""
    ch_client = init_ch_connection()
    init_clickhouse_db(ch_client)
    create_ch_table(ch_client)
    logging.info("created Clickhouse analytics tables from mongo")


if __name__ == "__main__":
    mongo_migrator()
