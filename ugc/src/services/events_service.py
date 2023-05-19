import logging
from datetime import datetime
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from fastapi import Depends

from core.config import settings
from db.kafka import get_kafka
from models import Event, EventPosted

logger = logging.getLogger(__name__)


class EventService:
    """Сервис для записи событий в Kafka"""

    def __init__(self, kafka_producer: AIOKafkaProducer):
        self.producer = kafka_producer

    async def send_event(self, event: Event) -> None:
        topic = event.type
        key = self._get_key(event)
        posted_event = EventPosted(
            **event.dict(), created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        try:
            await self.producer.send_and_wait(
                topic=topic, key=key.encode(), value=posted_event.json().encode()
            )
        except KafkaError as exc:
            logger.error(f"Kafka Error: {exc}")

    @staticmethod
    def _get_key(event):
        key = f"{event.user_id}:{event.movie_id}" if event.movie_id else event.user_id
        return key

    def _get_topic(self, event):
        topic = event.type
        print(self.producer.client.cluster.topics)
        if topic not in self.producer.client.cluster.topics():
            logger.warning(
                "Event topic not found in kafka, posting to default topic '%s'",
                settings.kafka_topic,
            )
            topic = settings.kafka_topic
        return topic


@lru_cache()
def get_events_service(kafka: AIOKafkaProducer = Depends(get_kafka)) -> EventService:
    return EventService(kafka)
