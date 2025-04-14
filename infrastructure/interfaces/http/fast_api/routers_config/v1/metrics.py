from typing import Annotated
from types import ModuleType
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from entities.metrics.metric import Metric as MetricEntity
from adapters.api.metrics.metric import MetricCreate, MetricPublic
from adapters.storage.sql_models.metric_group import MetricGroup
from adapters.storage.sql_models.metric import Metric
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

    @router.get("/", response_model=list[MetricPublic])
    async def list_metrics(safe_session: auth_dependency,
                           name: Annotated[str | None, Query(alias="name")] = None,
                           group_name: Annotated[str | None, Query(alias="group-name")] = None,
                           ) -> list[MetricPublic]:
        client, entities_storage_session = safe_session
        metric_repo = entities_repos_module.metric.Metric(entities_storage_session)
        filters = {}
        if name:
            filters = {Metric.name: name}
        if group_name:
            filters = {MetricGroup.name: group_name}
        metrics = metric_repo.get_list(filters)
        return [MetricPublic.from_entity(metric) for metric in metrics]

    @router.get("/{uuid_}", response_model=MetricPublic)
    async def get_metric(uuid_: UUID, safe_session: auth_dependency) -> MetricPublic:
        client, entities_storage_session = safe_session
        metric_repo = entities_repos_module.metric.Metric(entities_storage_session)
        metric = metric_repo.get_by_uuid(uuid_)
        return MetricPublic.from_entity(metric)

    @router.post("/", response_model=MetricPublic, status_code=status.HTTP_201_CREATED)
    async def create_metric(metric: MetricCreate, safe_session: auth_dependency) -> MetricPublic:
        client, entities_storage_session = safe_session
        metric_repo = entities_repos_module.metric.Metric(entities_storage_session)
        added_metric_entity = metric_repo.add(metric.to_entity()) # type: MetricEntity
        return MetricPublic.from_entity(added_metric_entity)

    return router
