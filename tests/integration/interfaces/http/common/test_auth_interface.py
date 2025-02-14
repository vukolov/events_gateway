from uuid import UUID
from tests.integration.interfaces.http.fixtures import *
from application.usecases.auth import Auth
from entities.clients.external_client import ExternalClient as ClientEntity


def test_auth_token(client, entities_storage, monkeypatch):
    monkeypatch.setattr(Auth, "authenticate_external_client", lambda *args: ClientEntity(UUID(int=0)))
    monkeypatch.setattr(Auth, "create_client_access_token", lambda *args: "test_token")
    response = client.post("/v1/auth/token",
                           data={"client_id": Auth.EFA_CONFIGURATION_CLIENT_ID, "client_secret": "test"},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "test_token", "token_type": "bearer"}
