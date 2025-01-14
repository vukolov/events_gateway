from abc import ABCMeta, abstractmethod
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from entities.metrics.metric_event import MetricEvent


class AbstractMetricEventsStorageSession(AbstractStorageSession, metaclass=ABCMeta):
    @abstractmethod
    def save_event(self, event_data: MetricEvent, topic: str):
        ...
