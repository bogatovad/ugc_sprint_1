import aiohttp
import clickhouse_driver
import pytest
from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka
from fastapi.testclient import TestClient
from models import Event

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
        Event(user_id=1, movie_id=1, movie_timestamp=50, type='view_progress'),
        Event(user_id=2, movie_id=2, movie_timestamp=25, type='view_progress'),
        Event(user_id=3, movie_id=3, movie_timestamp=75, type='view_progress')
    ]
    return data


@pytest.fixture
def make_post_request(session):
    async def inner(url, data):
        async with session.post(url, data=data) as response:
            response_data = await response.json()
            return response_data
    return inner


@pytest.fixture
def ch_conn():
    conn = clickhouse_driver.connect('clickhouse-node1')
    cursor = conn.cursor()


@pytest.fixture(scope="session")
def clickhouse_conn():
    conn = clickhouse_driver.connect(host='clickhouse-node1', port=9000)
    yield conn
    conn.cursor().execute('TRUNCATE TABLE cinema_analytics.movie_views')
    conn.close()

