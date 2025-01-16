from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
import auth
from adapters.api.metrics.metric_event import MetricEvent
from entities.users.user import User as UserEntity
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from application.usecases.metric_events_processor import MetricEventsProcessor


router = APIRouter(
    prefix="/metrics",
    dependencies=[Depends(auth.get_current_user)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/")
async def receive_metric(event: MetricEvent,
                         user: Annotated[UserEntity, Depends()],
                         entities_storage_session: Annotated[AbstractEntitiesStorageSession, Depends()],
                         metric_events_storage_session: Annotated[AbstractMetricEventsStorageSession, Depends()],
                         status_code=status.HTTP_201_CREATED):
    try:
        message_processor = MetricEventsProcessor(entities_storage_session, metric_events_storage_session, user)
        message_processor.send_to_downstream(event.to_entity())
        return {"status": "success", "message": "Metric sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
