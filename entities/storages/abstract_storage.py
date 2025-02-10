from typing import Generator
from abc import ABCMeta, abstractmethod
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession


class AbstractStorage(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self) -> Generator[AbstractStorageSession, None, None]:
        ...

    @abstractmethod
    def close(self) -> None:
        ...
