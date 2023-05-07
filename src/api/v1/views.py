from fastapi import APIRouter, HTTPException
from db.kafka_producer import producer
from models import ViewProgress


router = APIRouter()


@router.post("/progress")
async def write_view_progress(view_progress: ViewProgress):
    try:
        # Serialize the data to JSON and send it to Kafka
        producer.send(key=view_progress.id, value=view_progress.json().encode('utf-8'))
        return {"message": "View progress written to Kafka."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
