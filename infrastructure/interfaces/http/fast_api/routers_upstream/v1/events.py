from typing import Annotated
from types import ModuleType
from fastapi import APIRouter, HTTPException, status, Depends
from entities.users.user import User as UserEntity
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from application.usecases.metric_events_processor import MetricEventsProcessor
from application.storages.repositories.metric import Metric as AbstractMetricRepo
from adapters.api.metrics.metric_event import MetricEvent
from infrastructure.interfaces.http.fast_api.routers_common.v1.auth import TokenChecker


def init_events_router(token_checker: TokenChecker, metric_events_storage: AbstractEventsStorage, entities_repos_module: ModuleType) -> APIRouter:
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
    async def process_new_event(event: MetricEvent,
                                user: Annotated[UserEntity, Depends()],
                                safe_session: auth_dependency,
                                metric_events_storage_session: events_storage_dependency) -> None:
        try:
            client, entities_storage_session = safe_session
            metric_repo = entities_repos_module.metric.Metric(entities_storage_session)  # type: AbstractMetricRepo
            message_processor = MetricEventsProcessor(entities_storage_session, metric_events_storage_session, user)
            message_processor.send_to_downstream(event.to_entity(), metric_repo)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    return router
