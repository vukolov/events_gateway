import pytest
from uuid import UUID
from fastapi.testclient import TestClient
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.users.user import User as UserEntity
from entities.metrics.metric import Metric
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener


@pytest.fixture
def entities_storage_session(mocker):
    mock = mocker.Mock(name='entities_storage_session')
    mock.get_user.return_value = mocker.Mock(spec=UserEntity)
    mock.get_metric.return_value = mocker.Mock(spec=Metric,
                                               id=1,
                                               uuid="00000000-0000-0000-0000-000000000000",
                                               name="test",
                                               group_id=1,
                                               active=True)
    mock.get_metric_group.return_value = mocker.Mock()

    def metric_side_effect(metric_entity: Metric):
        return Metric(id=1,
                      uuid=UUID(int=0),
                      name=str(metric_entity.name),
                      group_id=metric_entity.group_id,
                      active=bool(metric_entity.active))
    mock.add_metric.side_effect = metric_side_effect

    result = mock.add_metric(Metric(UUID(int=0), "test"))
    assert isinstance(result, Metric)

    return mock


@pytest.fixture
def metric_events_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractMetricEventsStorageSession)
    return mock


@pytest.fixture
def entities_storage(mocker, entities_storage_session):
    mock = mocker.Mock(spec=AbstractEntitiesStorage)
    mock.create_session = lambda: (yield entities_storage_session)
    return mock


@pytest.fixture
def events_storage(mocker, metric_events_storage_session):
    mock = mocker.Mock(spec=AbstractEventsStorage)
    mock.create_session.return_value = metric_events_storage_session
    return mock


@pytest.fixture
async def client(entities_storage, events_storage, monkeypatch):
    assert callable(entities_storage.create_session)
    assert callable(events_storage.create_session)

    events_listener = EventsListener(events_storage, entities_storage)
    app = events_listener.get_instance()
    app.dependency_overrides[entities_storage.create_session] = lambda: entities_storage.create_session()
    app.dependency_overrides[events_storage.create_session] = lambda: events_storage.create_session()

    return TestClient(app)
