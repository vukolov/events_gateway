from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractTokenEncoder(metaclass=ABCMeta):
    @abstractmethod
    def encode(self, data: dict) -> str:
        ...

    @abstractmethod
    def decode(self, token: str) -> Any:
        ...
