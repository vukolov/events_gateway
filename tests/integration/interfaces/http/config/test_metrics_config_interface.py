import os
from uuid import UUID
from tests.integration.interfaces.http.fixtures import *
from entities.clients.external_client import ExternalClient as ClientEntity
from entities.metrics.metric import Metric
from application.usecases.auth import Auth
from infrastructure.interfaces.http.fast_api.jwt_encoder import JwtEncoder
from infrastructure.storages.entities.sql.repositories.metric import Metric as MetricRepo


def test_cli_token_authentication(client, monkeypatch):
    external_client = ClientEntity(UUID(int=0))
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
    monkeypatch.setattr(Auth, "get_client", lambda *args: ClientEntity(UUID(int=0)))
    monkeypatch.setattr(MetricRepo, "add", lambda *args: Metric(id=1,
                                                                uuid=UUID(int=0),
                                                                name="test"))
    headers = {
        "Authorization": f"Bearer doesntmatter",
    }
    payload = {
        "name": "test",
    }
    response = client.post("/v1/metrics", json=payload, headers=headers)

    assert response.status_code == 201
    response_data = response.json()

    assert "uuid" in response_data
    response_data.pop("uuid")

    assert response_data == {
        "name": "test",
        "group_name": "?",
        "active": False,
    }
