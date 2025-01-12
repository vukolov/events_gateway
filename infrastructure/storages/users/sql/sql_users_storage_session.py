from sqlmodel import Session, select
from entities.storage_sessions.abstract_users_storage_session import AbstractUsersStorageSession
from entities.user import User as UserEntity
from adapters.storage.sql.user import User as UserModel


class SqlUsersStorageSession(AbstractUsersStorageSession):
    def __init__(self, sqlmodel_session: Session):
        self._sqlmodel_session = sqlmodel_session

    def get_user(self, username: str) -> UserEntity:
        statement = select(UserModel).where(UserModel.username == username)
        results = self._sqlmodel_session.exec(statement)
        return results.one().to_entity()
