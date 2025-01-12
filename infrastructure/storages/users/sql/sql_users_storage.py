from sqlmodel import Session, create_engine
from entities.storages.abstract_users_storage import AbstractUsersStorage
from infrastructure.storages.users.sql.sql_users_storage_session import SqlUsersStorageSession


class SqlUsersStorage(AbstractUsersStorage):
    def __init__(self, connection_string: str):
        super().__init__()
        self._engine = create_engine(connection_string)

    def create_session(self) -> SqlUsersStorageSession:
        with Session(self._engine) as sqlmodel_session:
            yield SqlUsersStorageSession(sqlmodel_session)

    def close(self):
        """No need to close session for this case"""
        ...
