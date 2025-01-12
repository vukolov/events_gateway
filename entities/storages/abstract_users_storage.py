from abc import ABCMeta
from entities.storages.abstract_storage import AbstractStorage


class AbstractUsersStorage(AbstractStorage, metaclass=ABCMeta):
    ...
