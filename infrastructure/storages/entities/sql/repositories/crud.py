from typing import Type
from abc import ABCMeta, abstractmethod
from sqlmodel import select, SQLModel
from uuid import UUID
from entities.abstract_business_entity import AbstractBusinessEntity
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from application.storages.repositories.abstract_crud import AbstractCrud
from adapters.storage.abstract_model import AbstractModel


class Crud(AbstractCrud, metaclass=ABCMeta):
    @abstractmethod
    def _get_model(self) -> Type[AbstractModel]:
        ...

    def __init__(self, sql_session: AbstractStorageSession):
        self._model = self._get_model()
        self._sql_session = sql_session.get_session()

    def get_by_id(self, id_: int) -> AbstractBusinessEntity:
        model = self._sql_session.get(self._model, id_) # type: AbstractModel
        return model.to_entity()

    def get_by_uuid(self, uuid_: UUID) -> AbstractBusinessEntity:
        statement = select(self._model).where(self._model.uuid == uuid_)
        model = self._sql_session.exec(statement).one() # type: AbstractModel
        return model.to_entity()

    def add(self, entity: AbstractBusinessEntity) -> AbstractBusinessEntity:
        model = self._model.from_entity(entity)
        self._sql_session.add(model)
        self._sql_session.flush()
        self._sql_session.refresh(model)
        self._sql_session.commit()
        return model.to_entity()

    def update(self, entity: AbstractBusinessEntity) -> AbstractBusinessEntity:
        model_old = None
        if entity.id:
            model_old = self.get_by_id(entity.id)
        if not model_old:
            model_old = self.get_by_uuid(entity.uuid)
        if not model_old:
            raise ValueError("Entity not found")
        model_new = self._model.from_entity(entity)
        model_new.id = model_old.id
        model_new.uuid = model_old.uuid
        self._sql_session.add(model_new)
        self._sql_session.flush()
        self._sql_session.refresh(model_new)
        self._sql_session.commit()
        return model_new.to_entity()

    def delete_by_id(self, id_: int) -> None:
        ...