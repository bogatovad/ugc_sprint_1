import pytest


@pytest.mark.asyncio
async def test_write_view_progress(client, producer, make_post_request, sample_data):
    url = "http://ugc_api:8000/api/v1/progress"
    # Call the API endpoint with each item in the data list
    for item in sample_data:
        response = await make_post_request(url, data=item.json())
        # assert response.status_code == HTTPStatus.OK
        assert response == {"message": "View progress written to Kafka."}

        # Send the message to Kafka using the Kafka producer
        producer.send(key=item.id, value=item.json().encode('utf-8'))

    # Wait for the messages to be written to Kafka
    producer.flush()
