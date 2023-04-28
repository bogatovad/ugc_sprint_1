from kafka import KafkaProducer


class UGCKafkaProducer:

    def __init__(self) -> None:
        self.hosts = ['kafka:9092']
        self.topic = 'movies'# TODO move to settings
        self.producer = KafkaProducer(bootstrap_servers=self.hosts)

    def send(self, key, value):
        self.producer.send(self.topic, key, value)


producer = UGCKafkaProducer()

