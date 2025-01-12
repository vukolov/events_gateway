from abc import ABCMeta, abstractmethod
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from entities.user import User


class AbstractUsersStorageSession(AbstractStorageSession, metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, username: str) -> User:
        ...
