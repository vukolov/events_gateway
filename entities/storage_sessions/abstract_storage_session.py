from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractStorageSession(metaclass=ABCMeta):
    @abstractmethod
    def get_session(self) -> Any:
        ...
