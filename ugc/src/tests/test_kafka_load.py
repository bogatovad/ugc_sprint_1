from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_write_view_progress(client, producer, make_post_request, sample_data):
    url = "http://ugc_api:8000/api/v1/view_progress"
    # Call the API endpoint with each item in the data list
    for item in sample_data:
        response = await make_post_request(url, data=item.json())
        assert response == HTTPStatus.CREATED


