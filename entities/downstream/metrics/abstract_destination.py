from abc import ABCMeta, abstractmethod


class AbstractDestination(metaclass=ABCMeta):
    def __init__(self, address: str):
        self._address = address

    @abstractmethod
    def send(self, message: dict, topic: str):
        ...
