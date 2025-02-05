import os
import uuid
import secrets
import pytest
from application.usecases.auth import Auth
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.clients.external_client import ExternalClient
from infrastructure.interfaces.http.fast_api.jwt_encoder import JwtEncoder


client_uuid = uuid.UUID("f9ac15f6-a98d-402e-9417-31d028460066")
client_secret = secrets.token_urlsafe(64)
hashed_secret = Auth.hash_secret(client_secret)


@pytest.fixture
def entities_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractEntitiesStorageSession)

    def get_client_side_effect(client_uuid_):
        if client_uuid_ == client_uuid:
            client = ExternalClient(uuid=client_uuid_)
            client.hashed_secret = hashed_secret
            client.description = "test_client"
            return client
        else:
            return None

    mock.get_external_client.side_effect = get_client_side_effect
    return mock

def test_authenticate_external_client(entities_storage_session):
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    os.environ["EFA_CLI_SECRET_KEY"] = "some_secret"
    cli = auth.authenticate_external_client("cli", "some_secret", entities_storage_session)
    assert isinstance(cli, ExternalClient)

    not_existing_client = ExternalClient()
    assert auth.authenticate_external_client(str(not_existing_client.uuid), "", entities_storage_session) is False

    assert auth.authenticate_external_client(str(client_uuid), "wrong_secret", entities_storage_session) is False
    client = auth.authenticate_external_client(str(client_uuid), client_secret, entities_storage_session)
    assert isinstance(client, ExternalClient)
    assert client.description == "test_client"


def test_create_client_access_token():
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    client = ExternalClient(uuid=client_uuid)
    token = auth.create_client_access_token(client)
    decoded_token = token_encoder.decode(token)
    assert client.uuid == uuid.UUID(decoded_token["sub"])


def test_get_client(entities_storage_session):
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    client = ExternalClient(uuid=client_uuid)
    token = auth.create_client_access_token(client)
    found_client = auth.get_client(token, entities_storage_session)
    assert isinstance(found_client, ExternalClient)
    assert found_client.uuid == client.uuid

    unknown_client = ExternalClient(uuid=uuid.uuid4())
    token = auth.create_client_access_token(unknown_client)
    with pytest.raises(Exception) as e:
        auth.get_client(token, entities_storage_session)
