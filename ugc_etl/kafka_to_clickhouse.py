from clickhouse_driver import Client

from config import settings


client = Client(host=settings.clickhouse_host)


def init_clickhouse_db(client):
    client.execute(
        "CREATE DATABASE IF NOT EXISTS cinema_analytics ON CLUSTER company_cluster",
    )

    client.execute(
        """CREATE TABLE IF NOT EXISTS cinema_analytics.movie_views ON CLUSTER company_cluster(
        user_id String,
        movie_id String,
        movie_timestamp Int64         
        )
        Engine=MergeTree()
        ORDER BY movie_timestamp"""
    )


    client.execute(
        """CREATE TABLE IF NOT EXISTS cinema_analytics.kafka_movie_views(
            user_id String,
            movie_id String,
            movie_timestamp Int64
            )
            ENGINE = Kafka 
            SETTINGS
            kafka_broker_list = 'kafka:9092',
            kafka_topic_list = 'view_progress',
            kafka_group_name = 'clickhouse_reader',
            kafka_format = 'JSONEachRow',
            kafka_num_consumers = 1;"""
    )

    client.execute(
        """CREATE MATERIALIZED VIEW IF NOT EXISTS cinema_analytics.mv_kafka_movie_views TO cinema_analytics.movie_views AS
            SELECT * FROM cinema_analytics.kafka_movie_views;"""
    )

   

if __name__ == '__main__':
    init_clickhouse_db(client=client)