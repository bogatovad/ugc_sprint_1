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
        movie_timestamp Int64,
        type String,
        created_at Datetime         
        )
        Engine=MergeTree()
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at"""
    )


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
            kafka_num_consumers = 1;"""
    )

    client.execute(
        """CREATE MATERIALIZED VIEW IF NOT EXISTS cinema_analytics.mv_kafka_movie_views TO cinema_analytics.movie_views AS
            SELECT * FROM cinema_analytics.kafka_movie_views;"""
    )

   

if __name__ == '__main__':
    init_clickhouse_db(client=client)