from typing import Type, Any
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

    def get_list(self, filters: dict[Any, Any]) -> list[AbstractBusinessEntity]:
        statement = select(self._model)
        joined_models = set()

        for key, value in filters.items():
            if hasattr(key, 'class_') and key.class_ != self._model:
                rel_name = self._find_relationship_attr(key.class_)
                if rel_name:
                    if rel_name not in joined_models:
                        statement = statement.join(getattr(self._model, rel_name))
                        joined_models.add(rel_name)
            statement = statement.where(key == value)

        models = self._sql_session.exec(statement).all()
        return [model.to_entity() for model in models]

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

    def _find_relationship_attr(self, related_class: Type[AbstractModel]) -> str | None:
        for attr_name in dir(self._model):
            attr = getattr(self._model, attr_name)
            if hasattr(attr, 'property') and hasattr(attr.property, 'mapper'):
                if attr.property.mapper.class_ == related_class:
                    return attr_name
        return None