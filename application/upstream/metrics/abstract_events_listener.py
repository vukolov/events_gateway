from abc import ABCMeta, abstractmethod
from entities.storages.events_storage import EventsStorage
from entities.storages.users_storage import UsersStorage


class AbstractEventsListener(metaclass=ABCMeta):
    def __init__(self, events_storage: EventsStorage, users_storage: UsersStorage):
        self._events_storage = events_storage
        self._users_storage = users_storage

    @abstractmethod
    def run(self):
        ...
