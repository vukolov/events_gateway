from typing import Type
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from application.storages.repositories.metric import Metric as AbstractMetricRepo
from adapters.storage.sql_models.metric import Metric as MetricModel
from .crud import Crud


class Metric(AbstractMetricRepo, Crud):
    def __init__(self, session: AbstractStorageSession):
        AbstractMetricRepo.__init__(self, session)
        Crud.__init__(self, session)

    def _get_model(self) -> Type[MetricModel]:
        return MetricModel
