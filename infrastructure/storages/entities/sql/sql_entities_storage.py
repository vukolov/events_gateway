from sqlmodel import Session, create_engine
from typing import Generator
from contextlib import contextmanager
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from infrastructure.storages.entities.sql.sql_entities_storage_session import SqlEntitiesStorageSession


class SqlEntitiesStorage(AbstractEntitiesStorage):
    def __init__(self, connection_string: str | None = None):
        super().__init__()
        if connection_string is None:
            raise ValueError("Connection string is not provided")
        self._engine = create_engine(connection_string)

    @contextmanager
    def create_session(self) -> Generator[SqlEntitiesStorageSession, None, None]:
        with Session(self._engine) as sqlmodel_session:
            yield SqlEntitiesStorageSession(sqlmodel_session)

    def close(self) -> None:
        """No need to close session for this case"""
        ...
