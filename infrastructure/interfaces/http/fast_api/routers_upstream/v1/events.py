from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from entities.users.user import User as UserEntity
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from application.usecases.metric_events_processor import MetricEventsProcessor
from adapters.api.metrics.metric_event import MetricEvent
import infrastructure.interfaces.http.fast_api.routers_common.v1.auth as auth


def init_events_router(entities_storage: AbstractEntitiesStorage, metric_events_storage: AbstractEventsStorage):
    router = APIRouter(
        prefix="/v1/events",
        dependencies=[Depends(auth.get_current_client)],
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    entities_storage_session_dependency = Annotated[
        AbstractEntitiesStorageSession, Depends(entities_storage.create_session)]
    events_storage_dependency = Annotated[
        AbstractMetricEventsStorageSession, Depends(metric_events_storage.create_session)]

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def receive_metric(event: MetricEvent,
                             user: Annotated[UserEntity, Depends()],
                             entities_storage_session: entities_storage_session_dependency,
                             metric_events_storage_session: events_storage_dependency):
        try:
            message_processor = MetricEventsProcessor(entities_storage_session, metric_events_storage_session, user)
            message_processor.send_to_downstream(event.to_entity())
            return {}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    return router
