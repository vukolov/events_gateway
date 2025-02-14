from abc import ABCMeta
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession


class AbstractRepo(metaclass=ABCMeta):
    def __init__(self, session: AbstractStorageSession):
        self.session = session.get_session()
