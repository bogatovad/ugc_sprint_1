from ..main import app
from db.kafka_producer import UGCKafkaProducer
import aiohttp
from .settings import test_settings
import json
import pytest
from fastapi.testclient import TestClient
from models import ViewProgress

@pytest.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def producer() -> UGCKafkaProducer:
    return UGCKafkaProducer()


@pytest.fixture
def sample_data():
    data = [
        ViewProgress(user_id=1, movie_id=1, movie_timestamp=50),
        ViewProgress(user_id=2, movie_id=2, movie_timestamp=25),
        ViewProgress(user_id=3, movie_id=3, movie_timestamp=75)
    ]
    return data

# @pytest.fixture
# def make_get_request(session):
#     async def inner(endpoint: str, params: dict = {}) -> HTTPResponse:
#         url = f"{test_settings.service_url}{endpoint}"
#         async with session.get(url, params=params) as response:
#             return HTTPResponse(
#                 body=await response.json(),
#                 status=response.status,
#             )
#     return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url, data):
        async with session.post(url, data=json.dumps(data)) as response:
            response_data = await response.json()
            return response_data
    return inner
