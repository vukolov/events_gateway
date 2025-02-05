import os

import bcrypt
from uuid import UUID
from datetime import datetime, timedelta, timezone
from application.security.abstract_token_encoder import AbstractTokenEncoder
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient


class Auth:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    EFA_CONFIGURATION_CLIENT_ID = "cli"

    def __init__(self, token_encoder: AbstractTokenEncoder):
        self._token_encoder = token_encoder

    def authenticate_external_client(self, client_uuid: str, client_secret: str, clients_storage_session: AbstractEntitiesStorageSession) -> ExternalClient | bool:
        if client_uuid == self.EFA_CONFIGURATION_CLIENT_ID:
            if client_secret == os.getenv("EFA_CLI_SECRET_KEY"):
                return ExternalClient()
            return False
        try:
            client_uuid = UUID(client_uuid)
        except ValueError:
            return False
        client = clients_storage_session.get_external_client(client_uuid)
        if client is None:
            return False
        if not self._verify_secret_key(client_secret, client.hashed_secret):
            return False
        return client

    def create_client_access_token(self, client: ExternalClient) -> str:
        to_encode = {
            "sub": str(client.uuid),
            # "scope": client.scope,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return self._token_encoder.encode(to_encode)

    def get_client(self, token: str, clients_storage_session: AbstractEntitiesStorageSession) -> ExternalClient:
        payload = self._token_encoder.decode(token)
        uuid: str = payload.get("sub")
        if uuid is None:
            raise Exception("Could not validate credentials")
        client = clients_storage_session.get_external_client(UUID(uuid))
        if client is None:
            raise Exception("No such client")
        return client

    @staticmethod
    def hash_secret(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_secret_key(self, received_secret: str, hashed_secret: str) -> bool:
        return bcrypt.checkpw(received_secret.encode('utf-8'), hashed_secret.encode('utf-8'))
