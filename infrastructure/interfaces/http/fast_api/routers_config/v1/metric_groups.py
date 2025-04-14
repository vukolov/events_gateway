from typing import Annotated
from types import ModuleType
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity
from adapters.api.metrics.metric_group import MetricGroupCreate, MetricGroupPublic
from infrastructure.interfaces.http.fast_api.routers_common.v1.auth import TokenChecker


def init_metric_groups_router(token_checker: TokenChecker, entities_repos_module: ModuleType) -> APIRouter:
    router = APIRouter(
        prefix="/v1/metric-groups",
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    auth_dependency = Annotated[
        tuple[ExternalClient, AbstractEntitiesStorageSession],
        Depends(token_checker.get_safe_session)
    ]

    @router.get("/", response_model=list[MetricGroupPublic])
    async def list_metric_groups(safe_session: auth_dependency) -> list[MetricGroupPublic]:
        client, entities_storage_session = safe_session
        metric_group_repo = entities_repos_module.metric_group.MetricGroup(entities_storage_session)
        # filters = {}
        # if group_name:
        #     filters = {"group.name": group_name}
        metrics = metric_group_repo.get_list({})
        return [MetricGroupPublic.from_entity(metric) for metric in metrics]

    @router.get("/{uuid_}", response_model=MetricGroupPublic)
    async def get_metric_group(uuid_: UUID, safe_session: auth_dependency) -> MetricGroupPublic:
        client, entities_storage_session = safe_session
        metric_group_repo = entities_repos_module.metric_group.MetricGroup(entities_storage_session)
        metric_group = metric_group_repo.get_by_uuid(uuid_)
        return MetricGroupPublic.from_entity(metric_group)

    @router.post("/", response_model=MetricGroupPublic, status_code=status.HTTP_201_CREATED)
    async def create_metric(metric_group: MetricGroupCreate, safe_session: auth_dependency) -> MetricGroupPublic:
        client, entities_storage_session = safe_session
        metric_group_repo = entities_repos_module.metric_group.MetricGroup(entities_storage_session)
        added_metric_entity = metric_group_repo.add(metric_group.to_entity()) # type: MetricGroupEntity
        return MetricGroupPublic.from_entity(added_metric_entity)

    return router
