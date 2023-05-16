import json

import aiohttp
import pytest
from aiokafka import AIOKafkaProducer
from fastapi.testclient import TestClient
from models import ViewProgress
from src.db.kafka import get_kafka

from ..main import app


@pytest.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
async def producer() -> AIOKafkaProducer:
    producer = await get_kafka()
    return producer


@pytest.fixture
def sample_data():
    data = [
        ViewProgress(user_id=1, movie_id=1, movie_timestamp=50, type='view_progress'),
        ViewProgress(user_id=2, movie_id=2, movie_timestamp=25, type='view_progress'),
        ViewProgress(user_id=3, movie_id=3, movie_timestamp=75, type='view_progress')
    ]
    return data


@pytest.fixture
def make_post_request(session):
    async def inner(url, data):
        async with session.post(url, data=json.dumps(data)) as response:
            response_data = await response.json()
            return response_data
    return inner
