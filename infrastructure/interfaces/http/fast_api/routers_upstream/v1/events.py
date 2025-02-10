from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from entities.users.user import User as UserEntity
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from application.usecases.metric_events_processor import MetricEventsProcessor
from adapters.api.metrics.metric_event import MetricEvent
from infrastructure.interfaces.http.fast_api.routers_common.v1.auth import TokenChecker


def init_events_router(token_checker: TokenChecker, metric_events_storage: AbstractEventsStorage):
    router = APIRouter(
        prefix="/v1/events",
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    auth_dependency = Annotated[
        tuple[ExternalClient, AbstractEntitiesStorageSession],
        Depends(token_checker.get_safe_session)
    ]
    events_storage_dependency = Annotated[
        AbstractMetricEventsStorageSession, Depends(metric_events_storage.create_session)
    ]

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def receive_metric(event: MetricEvent,
                             user: Annotated[UserEntity, Depends()],
                             safe_session: auth_dependency,
                             metric_events_storage_session: events_storage_dependency):
        try:
            client, entities_storage_session = safe_session
            message_processor = MetricEventsProcessor(entities_storage_session, metric_events_storage_session, user)
            message_processor.send_to_downstream(event.to_entity())
            return {}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    return router
