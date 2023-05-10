from clickhouse_driver import Client
#from kafka import KafkaConsumer


from clickhouse import init_clickhouse_db, create_kafka_integration, create_mv
from config import settings


client = Client(host=settings.clickhouse_host)


def etl_process():
    init_clickhouse_db(client=client)
    create_kafka_integration(client=client)
    create_mv(client=client)
    


if __name__ == '__main__':
    etl_process()