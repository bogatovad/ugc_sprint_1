from typing import ByteString

from kafka import KafkaProducer

from core.config import settings


class UGCKafkaProducer:
    """A Kafka producer for sending messages to a Kafka topic."""

    def __init__(self) -> None:
        self.hosts = [f'{settings.kafka_host}:{settings.kafka_port}']
        self.topic = settings.topic_name
        self.producer = KafkaProducer(bootstrap_servers=self.hosts)

    def send(self, key: ByteString, value: ByteString) -> None:
        self.producer.send(self.topic, key=key, value=value)

    def start(self) -> None:
        self.producer._wait_on_metadata(self.topic, max_wait=120)

    def stop(self) -> None:
        self.producer.close()


producer = UGCKafkaProducer()
