from typing import Type
from entities.storage_sessions.abstract_storage_session import AbstractStorageSession
from application.storages.repositories.external_client import ExternalClient as AbstractClientRepo
from adapters.storage.sql_models.external_client import ExternalClient as ClientModel
from .crud import Crud


class ExternalClient(AbstractClientRepo, Crud):
    def __init__(self, session: AbstractStorageSession):
        AbstractClientRepo.__init__(self, session)
        Crud.__init__(self, session)

    def _get_model(self) -> Type[ClientModel]:
        return ClientModel
