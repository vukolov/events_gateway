import pytest
from fastapi.testclient import TestClient
from application.usecases.metric_events_processor import MetricEventsProcessor
from application.usecases.auth import Auth
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.users.user import User as UserEntity
from entities.clients.external_client import ExternalClient as ClientEntity
from entities.metrics.metric import Metric
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener
import infrastructure.interfaces.http.fast_api.routers_common.v1.auth as auth


@pytest.fixture
def entities_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractEntitiesStorageSession)
    mock.get_user.return_value = mocker.Mock(spec=UserEntity)
    mock.get_metric.return_value = mocker.Mock(spec=Metric,
                                               id=1,
                                               uuid="00000000-0000-0000-0000-000000000000",
                                               name="test",
                                               group_id=1,
                                               active=True)
    mock.get_metric_group.return_value = mocker.Mock()
    return mock


@pytest.fixture
def metric_events_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractMetricEventsStorageSession)
    return mock


@pytest.fixture
def entities_storage(mocker, entities_storage_session):
    mock = mocker.Mock(spec=AbstractEntitiesStorage)
    mock.create_session = mocker.Mock(return_value=entities_storage_session)
    return mock


@pytest.fixture
def events_storage(mocker, metric_events_storage_session):
    mock = mocker.Mock(spec=AbstractEventsStorage)
    mock.create_session.return_value = metric_events_storage_session
    return mock


@pytest.fixture
async def client(entities_storage, events_storage):
    assert callable(entities_storage.create_session)
    assert callable(events_storage.create_session)

    assert isinstance(entities_storage.create_session(), AbstractEntitiesStorageSession)

    events_listener = EventsListener(events_storage, entities_storage)
    app = events_listener.get_instance()
    app.dependency_overrides[entities_storage.create_session] = lambda: entities_storage.create_session()
    app.dependency_overrides[events_storage.create_session] = lambda: events_storage.create_session()
    app.dependency_overrides[auth.get_current_client] = lambda: ClientEntity()

    return TestClient(app)


def test_metrics_event(client, monkeypatch):
    monkeypatch.setattr(Auth, "authenticate_external_client", lambda *args: ClientEntity())
    monkeypatch.setattr(MetricEventsProcessor, "send_to_downstream", lambda *args: None)
    # Define the payload for the event
    payload = {
        "metric_uuid": "00000000-0000-0000-0000-000000000000",
        "event_time": "2025-01-01 00:00:00",
        "metric_value": 0.01,
    }
    # Send a POST request to the events listener endpoint
    response = client.post("/v1/events", json=payload)

    # Check the response status code and content
    assert response.status_code == 201
    assert response.json() == {}


def test_auth_token(client, entities_storage, monkeypatch):
    monkeypatch.setattr(Auth, "authenticate_external_client", lambda *args: ClientEntity())
    monkeypatch.setattr(Auth, "create_client_access_token", lambda *args: "test_token")
    response = client.post("/v1/auth/token",
                           data={"client_id": "cli", "client_secret": "test"},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "test_token", "token_type": "bearer"}
