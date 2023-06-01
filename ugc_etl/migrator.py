from kafka_to_clickhouse import kafka_migrator
from mongo_to_clickhouse import mongo_migrator

if __name__ == "__main__":
    kafka_migrator()
    mongo_migrator()
