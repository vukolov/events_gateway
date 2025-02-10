from sqlmodel import Session, create_engine
from typing import Generator
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from infrastructure.storages.entities.sql.sql_entities_storage_session import SqlEntitiesStorageSession


class SqlEntitiesStorage(AbstractEntitiesStorage):
    def __init__(self, connection_string: str):
        super().__init__()
        self._engine = create_engine(connection_string)

    def create_session(self) -> Generator[SqlEntitiesStorageSession, None, None]:
        with Session(self._engine) as sqlmodel_session:
            yield SqlEntitiesStorageSession(sqlmodel_session)

    def close(self):
        """No need to close session for this case"""
        ...
