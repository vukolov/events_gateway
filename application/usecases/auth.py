import os
import bcrypt
from typing import cast
from uuid import UUID
from datetime import datetime, timedelta, timezone
from entities.clients.external_client import ExternalClient
from application.security.abstract_token_encoder import AbstractTokenEncoder
from application.storages.repositories.external_client import ExternalClient as ExternalClientRepo


class Auth:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    EFA_CONFIGURATION_CLIENT_ID = "cli"

    def __init__(self, token_encoder: AbstractTokenEncoder):
        self._token_encoder = token_encoder

    def authenticate_external_client(self, client_uuid_str: str, client_secret: str, clients_repo: ExternalClientRepo) -> ExternalClient | None:
        if client_uuid_str == self.EFA_CONFIGURATION_CLIENT_ID:
            if client_secret == os.getenv("EFA_CLI_SECRET_KEY"):
                return ExternalClient(uuid=UUID(int=0))
            return None
        try:
            client_uuid = UUID(client_uuid_str)
        except ValueError:
            return None
        client = cast(ExternalClient, clients_repo.get_by_uuid(client_uuid))
        if client is None or client.hashed_secret is None:
            return None
        if not self._verify_secret_key(client_secret, client.hashed_secret):
            return None
        return client

    def create_client_access_token(self, client: ExternalClient) -> str:
        to_encode = {
            "sub": str(client.uuid),
            # "scope": client.scope,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return self._token_encoder.encode(to_encode)

    def get_client(self, token: str, clients_repo: ExternalClientRepo) -> ExternalClient:
        payload = self._token_encoder.decode(token)
        uuid_str: str = payload.get("sub")
        if uuid_str is None:
            raise Exception("Could not validate credentials")
        uuid = UUID(uuid_str)
        if uuid == UUID(int=0):
            return ExternalClient(uuid=uuid)
        client = cast(ExternalClient, clients_repo.get_by_uuid(uuid))
        if client is None:
            raise Exception("No such client")
        return client

    @staticmethod
    def hash_secret(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_secret_key(self, received_secret: str, hashed_secret: str) -> bool:
        return bcrypt.checkpw(received_secret.encode('utf-8'), hashed_secret.encode('utf-8'))
