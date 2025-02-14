from uuid import UUID
from application.usecases.metric_events_processor import MetricEventsProcessor
from tests.integration.interfaces.http.fixtures import *
from application.usecases.auth import Auth
from entities.clients.external_client import ExternalClient as ClientEntity


def test_metrics_event(client, monkeypatch):
    monkeypatch.setattr(Auth, "get_client", lambda *args: ClientEntity(UUID(int=0)))
    monkeypatch.setattr(MetricEventsProcessor, "send_to_downstream", lambda *args: None)
    headers = {
        "Authorization": f"Bearer doesntmatter",
    }
    payload = {
        "metric_uuid": "00000000-0000-0000-0000-000000000000",
        "event_time": "2025-01-01 00:00:00",
        "metric_value": 0.01,
    }
    response = client.post("/v1/events", json=payload, headers=headers)

    assert response.status_code == 201
