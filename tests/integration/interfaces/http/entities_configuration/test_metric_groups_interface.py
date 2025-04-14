from uuid import UUID
from tests.integration.interfaces.http.fixtures import *
from entities.clients.external_client import ExternalClient as ClientEntity
from entities.metrics.metric_group import MetricGroup
from application.usecases.auth import Auth
from infrastructure.storages.entities.sql.repositories.metric_group import MetricGroup as MetricGroupRepo


def test_get_metric_list(client, monkeypatch):
    monkeypatch.setattr(Auth, "get_client", lambda *args: ClientEntity(UUID(int=0)))
    headers = {
        "Authorization": f"Bearer doesntmatter",
    }
    groups_list = [
        MetricGroup(id=1, uuid=UUID(int=0), name="test", user_id=0, measure_frequency_id=0, active=False),
        MetricGroup(id=2, uuid=UUID(int=1), name="test1", user_id=0, measure_frequency_id=0, active=False)]
    monkeypatch.setattr(MetricGroupRepo, "get_list", lambda *args: groups_list)
    response = client.get("/v1/metric-groups", headers=headers)

    assert response.status_code == 200


def test_create_metric_group(client, monkeypatch):
    monkeypatch.setattr(Auth, "get_client", lambda *args: ClientEntity(UUID(int=0)))
    monkeypatch.setattr(MetricGroupRepo, "add", lambda *args: MetricGroup(id=1,
                                                                          uuid=UUID(int=0),
                                                                          name="test",
                                                                          user_id=0,
                                                                          measure_frequency_id=0,
                                                                          active=False))
    headers = {
        "Authorization": f"Bearer doesntmatter",
    }
    payload = {
        "name": "test",
    }
    response = client.post("/v1/metric-groups", json=payload, headers=headers)

    assert response.status_code == 201
    response_data = response.json()

    assert "uuid" in response_data
    response_data.pop("uuid")

    assert response_data == {
        "name": "test",
        "group_name": "?",
        "active": False,
    }
