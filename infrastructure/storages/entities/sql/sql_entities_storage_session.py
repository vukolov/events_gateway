from sqlmodel import Session, select
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession


class SqlEntitiesStorageSession(AbstractEntitiesStorageSession):
    def __init__(self, sqlmodel_session: Session):
        self._sqlmodel_session = sqlmodel_session

    def get_session(self) -> Session:
        return self._sqlmodel_session
