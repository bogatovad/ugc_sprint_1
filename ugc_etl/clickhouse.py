from clickhouse_driver import Client

from config import settings


client = Client(host=settings.clickhouse_host)


def create_tables(client):
    client.execute(
        """CREATE TABLE IF NOT EXISTS movie_views ON CLUSTER company_cluster(
        id Int64,
        user_id String,
        film_id String,
        movie_timestamp Int64         
        )
        Engine=MergeTree()
        ORDER BY movie_timestamp"""
    )


def insert_to_clickhouse(client, values: list):
    client.execute('INSERT INTO movie_views(...) VALUES (values)')
