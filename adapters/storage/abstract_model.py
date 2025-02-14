from abc import ABCMeta, abstractmethod
from typing import Any
from uuid import UUID
from entities.abstract_business_entity import AbstractBusinessEntity


class AbstractModel(metaclass=ABCMeta):
    id: int | None
    uuid: UUID

    @abstractmethod
    def to_entity(self) -> AbstractBusinessEntity:
        ...

    @staticmethod
    @abstractmethod
    def from_entity(entity: Any) -> "AbstractModel":
        ...
