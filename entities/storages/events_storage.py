from abc import ABCMeta, abstractmethod
from entities.storages.abstract_storage import AbstractStorage


class AbstractEventsStorage(AbstractStorage, metaclass=ABCMeta):
    ...
