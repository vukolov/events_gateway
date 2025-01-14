from abc import ABCMeta, abstractmethod
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from entities.users.user import User
from entities.metrics.metric import Metric
from entities.metrics.metric_group import MetricGroup


class AbstractEntitiesStorageSession(AbstractStorageSession, metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, username: str) -> User:
        ...

    @abstractmethod
    def get_metric(self, metric_uuid: str) -> Metric:
        ...

    @abstractmethod
    def get_metric_group(self, group_id: int) -> MetricGroup:
        ...
