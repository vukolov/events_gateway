import os
import secrets
import pytest
from uuid import UUID, uuid4
from entities.clients.external_client import ExternalClient
from application.usecases.auth import Auth
from application.storages.repositories.external_client import ExternalClient as ExternalClientRepo
from infrastructure.interfaces.http.fast_api.jwt_encoder import JwtEncoder


client_uuid = UUID("f9ac15f6-a98d-402e-9417-31d028460066")
client_secret = secrets.token_urlsafe(64)
hashed_secret = Auth.hash_secret(client_secret)


@pytest.fixture
def clients_storage_repo(mocker):
    client = ExternalClient(uuid=client_uuid)
    mock = mocker.Mock(spec=ExternalClientRepo)
    mock.get_by_id.return_value = client

    def get_client_side_effect(client_uuid_):
        if client_uuid_ == client_uuid:
            client = ExternalClient(uuid=client_uuid_)
            client.hashed_secret = hashed_secret
            client.description = "test_client"
            return client
        else:
            return None

    mock.get_by_uuid.side_effect = get_client_side_effect
    return mock

def test_authenticate_external_client(clients_storage_repo):
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    os.environ["EFA_CLI_SECRET_KEY"] = "some_secret"
    cli = auth.authenticate_external_client(Auth.EFA_CONFIGURATION_CLIENT_ID,
                                            "some_secret",
                                            clients_storage_repo)
    assert isinstance(cli, ExternalClient)
    assert cli.uuid == UUID(int=0)

    not_existing_client = ExternalClient(UUID(int=0))
    assert auth.authenticate_external_client(str(not_existing_client.uuid), "", clients_storage_repo) is None

    assert auth.authenticate_external_client(str(client_uuid), "wrong_secret", clients_storage_repo) is None
    client = auth.authenticate_external_client(str(client_uuid), client_secret, clients_storage_repo)
    assert isinstance(client, ExternalClient)
    assert client.description == "test_client"


def test_create_client_access_token():
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    client = ExternalClient(uuid=client_uuid)
    token = auth.create_client_access_token(client)
    decoded_token = token_encoder.decode(token)
    assert client.uuid == UUID(decoded_token["sub"])


def test_get_client(clients_storage_repo):
    token_encoder = JwtEncoder("123", "HS256")
    auth = Auth(token_encoder)
    client = ExternalClient(uuid=client_uuid)
    token = auth.create_client_access_token(client)
    found_client = auth.get_client(token, clients_storage_repo)
    assert isinstance(found_client, ExternalClient)
    assert found_client.uuid == client.uuid

    unknown_client = ExternalClient(uuid=uuid4())
    token = auth.create_client_access_token(unknown_client)
    with pytest.raises(Exception) as e:
        auth.get_client(token, clients_storage_repo)
