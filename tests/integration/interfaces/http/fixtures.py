import importlib
from contextlib import closing, contextmanager
import pytest
from fastapi.testclient import TestClient
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener


@pytest.fixture
def entities_storage_session(mocker):
    mock = mocker.Mock(name='entities_storage_session')
    return mock


@pytest.fixture
def metric_events_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractMetricEventsStorageSession)
    return mock


@pytest.fixture
def entities_storage(mocker, entities_storage_session):
    @contextmanager
    def mock_create_session():
        yield entities_storage_session

    mock = mocker.Mock(spec=AbstractEntitiesStorage)
    mock.create_session = mock_create_session
    # mock.close.return_value = None
    return mock


@pytest.fixture
def events_storage(mocker, metric_events_storage_session):
    mock = mocker.Mock(spec=AbstractEventsStorage)

    @contextmanager
    def mock_create_session():
        yield metric_events_storage_session

    mock.create_session = mock_create_session
    # mock.close.return_value = None
    return mock


@pytest.fixture
async def client(entities_storage, events_storage, monkeypatch):
    assert callable(entities_storage.create_session)
    assert callable(events_storage.create_session)

    entities_repos_path = "infrastructure.storages.entities.sql.repositories"
    repos_module = importlib.import_module(entities_repos_path)

    def override_create_entities_session():
        with closing(entities_storage.create_session()) as session_gen:
            yield next(session_gen)


    def override_create_events_session():
        with closing(events_storage.create_session()) as session_gen:
            yield next(session_gen)

    events_listener = EventsListener(events_storage, entities_storage, repos_module)
    app = events_listener.get_instance()
    app.dependency_overrides[entities_storage.create_session] = override_create_entities_session
    app.dependency_overrides[events_storage.create_session] = override_create_events_session

    return TestClient(app)
