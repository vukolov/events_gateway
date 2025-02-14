from typing import Annotated
from types import ModuleType
from fastapi import APIRouter, status, Depends
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from entities.metrics.metric import Metric as MetricEntity
from adapters.api.metrics.metric import MetricCreate, MetricPublic
from infrastructure.interfaces.http.fast_api.routers_common.v1.auth import TokenChecker


def init_metrics_router(token_checker: TokenChecker, entities_repos_module: ModuleType) -> APIRouter:
    router = APIRouter(
        prefix="/v1/metrics",
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    auth_dependency = Annotated[
        tuple[ExternalClient, AbstractEntitiesStorageSession],
        Depends(token_checker.get_safe_session)
    ]

    @router.post("/", response_model=MetricPublic, status_code=status.HTTP_201_CREATED)
    async def create_metric(metric: MetricCreate, safe_session: auth_dependency) -> MetricPublic:
        client, entities_storage_session = safe_session
        metric_repo = entities_repos_module.metric.Metric(entities_storage_session)
        added_metric_entity = metric_repo.add(metric.to_entity()) # type: MetricEntity
        return MetricPublic.from_entity(added_metric_entity)

    return router
