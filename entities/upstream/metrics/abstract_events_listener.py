from abc import ABCMeta, abstractmethod
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage


class AbstractEventsListener(metaclass=ABCMeta):
    def __init__(self, events_storage: AbstractEventsStorage, users_storage: AbstractEntitiesStorage):
        self._events_storage = events_storage
        self._users_storage = users_storage

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def get_instance(self) -> object:
        ...
