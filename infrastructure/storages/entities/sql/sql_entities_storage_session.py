from sqlmodel import Session, select
from uuid import UUID
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.clients.external_client import ExternalClient as ExternalClientEntity
from adapters.storage.sql_models.user import User as UserModel
from adapters.storage.sql_models.external_client import ExternalClient as ExternalClientModel


class SqlEntitiesStorageSession(AbstractEntitiesStorageSession):
    def __init__(self, sqlmodel_session: Session):
        self._sqlmodel_session = sqlmodel_session

    def get_session(self) -> Session:
        return self._sqlmodel_session
    #
    # def get_external_client(self, client_uuid: UUID) -> ExternalClientEntity:
    #     statement = select(ExternalClientModel).where(ExternalClientModel.uuid == client_uuid)
    #     return self._sqlmodel_session.exec(statement).one().to_entity()

