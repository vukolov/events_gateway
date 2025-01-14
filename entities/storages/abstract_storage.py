from abc import ABCMeta, abstractmethod
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession


class AbstractStorage(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self) -> AbstractStorageSession:
        ...

    @abstractmethod
    def close(self):
        ...
