from abc import ABCMeta, abstractmethod
from uuid import UUID
from entities.abstract_business_entity import AbstractBusinessEntity


class AbstractCrud(metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, id_: int) -> AbstractBusinessEntity:
        ...

    @abstractmethod
    def get_by_uuid(self, uuid_: UUID) -> AbstractBusinessEntity:
        ...

    @abstractmethod
    def add(self, entity: AbstractBusinessEntity) -> AbstractBusinessEntity:
        ...

    @abstractmethod
    def update(self, entity: AbstractBusinessEntity) -> AbstractBusinessEntity:
        ...

    @abstractmethod
    def delete_by_id(self, id_: int) -> None:
        ...