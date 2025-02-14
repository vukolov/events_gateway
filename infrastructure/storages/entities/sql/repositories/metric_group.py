from typing import Type
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from application.storages.repositories.metric_group import MetricGroup as AbstractMetricGroupRepo
from adapters.storage.sql_models.metric_group import MetricGroup as MetricGroupModel
from .crud import Crud


class MetricGroup(AbstractMetricGroupRepo, Crud):
    def __init__(self, session: AbstractStorageSession):
        AbstractMetricGroupRepo.__init__(self, session)
        Crud.__init__(self, session)

    def _get_model(self) -> Type[MetricGroupModel]:
        return MetricGroupModel
