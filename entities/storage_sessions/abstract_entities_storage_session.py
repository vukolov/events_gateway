from abc import ABCMeta
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession


class AbstractEntitiesStorageSession(AbstractStorageSession, metaclass=ABCMeta):
    ...
