from tests.integration.interfaces.http.fixtures import *
import os
from application.usecases.auth import Auth
from infrastructure.interfaces.http.fast_api.jwt_encoder import JwtEncoder
from entities.clients.external_client import ExternalClient as ClientEntity


def test_cli_token_authentication(client, monkeypatch):
    external_client = ClientEntity()
    external_client.uuid = "00000000-0000-0000-0000-000000000000"
    token_encoder = JwtEncoder(os.getenv("UPSTREAM_SECURITY_TOKEN_SECRET"),
                               os.getenv("UPSTREAM_SECURITY_TOKEN_ALGORITHM"))
    auth = Auth(token_encoder)
    access_token = auth.create_client_access_token(external_client)
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "name": "test",
    }
    response = client.post("/v1/metrics", json=payload, headers=headers)

    assert response.status_code == 201

def test_create_metric(client, monkeypatch):
    monkeypatch.setattr(Auth, "get_client", lambda *args: ClientEntity())
    headers = {
        "Authorization": f"Bearer doesntmatter",
    }
    payload = {
        "name": "test",
    }
    response = client.post("/v1/metrics", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json() == {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "name": "test",
        "group_name": "?",
        "active": False,
    }
