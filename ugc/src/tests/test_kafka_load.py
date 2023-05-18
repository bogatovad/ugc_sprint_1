from http import HTTPStatus

import pytest
from models import Event

from .settings import test_settings


@pytest.mark.asyncio
async def test_write_view_progress(make_post_request, sample_data, clickhouse_conn):

    # Call the API endpoint with each item in the data list
    for item in sample_data:
        response = await make_post_request(test_settings.view_progress_url, data=item.json())
        assert response == HTTPStatus.CREATED

    cursor = clickhouse_conn.cursor()
    cursor.execute(f'SELECT * FROM {test_settings.clickhouse_table}')

    ch_events = []
    for row in cursor:
        ch_events.append(Event(user_id=row[0], movie_id=str(row[1]), movie_timestamp=row[2], type=row[3]))

    assert all(event in sample_data for event in ch_events)



