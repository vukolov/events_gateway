from fastapi import APIRouter, Depends, HTTPException, status, Depends
import auth
from adapters.api.metrics.metric_event import MetricEvent


router = APIRouter(
    prefix="/metrics",
    dependencies=[Depends(auth.get_current_user)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/")
async def receive_metric(event: MetricEvent, status_code=status.HTTP_201_CREATED):
    try:
        ...
        # event_dict = event.dict()
        # send_to_kafka(event_dict)
        # return {"status": "success", "message": "Metric sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")