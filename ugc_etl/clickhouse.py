from clickhouse_driver import Client

from config import settings


client = Client(host=settings.clickhouse_host)


def init_clickhouse_db(client):
    client.execute(
        "CREATE DATABASE IF NOT EXISTS cinema_analytics ON CLUSTER company_cluster",
    )

    client.execute(
        """CREATE TABLE IF NOT EXISTS cinema_analytics.movie_views ON CLUSTER company_cluster(
        id Int64,
        user_id String,
        film_id String,
        movie_timestamp Int64         
        )
        Engine=MergeTree()
        ORDER BY movie_timestamp"""
    )


def create_kafka_integration(client):
    client.execute(
        """CREATE TABLE IF NOT EXISTS cinema_analytics.kafka_movie_views(
            id Int64,
            user_id String,
            film_id String,
            movie_timestamp Int64
            )
            ENGINE = Kafka 
            SETTINGS
            kafka_broker_list = 'broker:29092',
            kafka_topic_list = 'film_views',
            kafka_group_name = 'clickhouse_reader',
            kafka_format = 'JSONEachRow',
            kafka_num_consumers = 1;"""
    )


def create_mv(client):
    client.execute(
        """CREATE MATERIALIZED VIEW IF NOT EXISTS cinema_analytics.mv_kafka_movie_views TO cinema_analytics.movie_views AS
            SELECT * FROM cinema_analytics.kafka_movie_views;"""
    )


# def insert_to_clickhouse(client, values: list):
#    client.execute('INSERT INTO movie_views(...) VALUES (values)')
