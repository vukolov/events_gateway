from abc import ABCMeta, abstractmethod


class AbstractStorageSession(metaclass=ABCMeta):
    @abstractmethod
    def close(self):
        ...
