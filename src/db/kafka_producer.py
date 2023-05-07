from kafka import KafkaProducer
from core.config import settings


class UGCKafkaProducer:

    def __init__(self) -> None:
        self.hosts = [f'{settings.kafka_host}:{settings.kafka_port}']
        self.topic = 'view_progress'# TODO move to settings
        self.producer = KafkaProducer(bootstrap_servers=self.hosts)

    def send(self, key, value):
        self.producer.send(self.topic, key=key, value=value)


producer = UGCKafkaProducer()

