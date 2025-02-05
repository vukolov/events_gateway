from abc import ABCMeta, abstractmethod
from uuid import UUID
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from entities.users.user import User
from entities.clients.external_client import ExternalClient
from entities.metrics.metric import Metric
from entities.metrics.metric_group import MetricGroup


class AbstractEntitiesStorageSession(AbstractStorageSession, metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, username: str) -> User:
        ...

    @abstractmethod
    def get_external_client(self, client_uuid: UUID) -> ExternalClient:
        ...

    @abstractmethod
    def get_metric(self, metric_uuid: UUID) -> Metric:
        ...

    @abstractmethod
    def get_metric_group(self, group_id: int) -> MetricGroup:
        ...
