import pytest
from uuid import UUID
from application.usecases.metric_events_processor import MetricEventsProcessor
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.users.plan import Plan
from entities.metrics.metric_event import MetricEvent
from entities.metrics.measure_frequency import MeasureFrequency
from infrastructure.storages.entities.sql.repositories.metric import Metric as MetricRepo


@pytest.fixture
def entities_storage_session(mocker):
    return mocker.Mock(spec=AbstractEntitiesStorageSession)


@pytest.fixture
def metric_events_storage_session(mocker):
    return mocker.Mock(spec=AbstractMetricEventsStorageSession)


@pytest.fixture
def user(mocker):
    return mocker.Mock(spec=UserEntity)


@pytest.fixture
def processor(entities_storage_session, metric_events_storage_session, user):
    return MetricEventsProcessor(entities_storage_session, metric_events_storage_session, user)


def test_send_to_downstream(processor, metric_events_storage_session, mocker):
    metric_event = mocker.Mock(spec=MetricEvent)
    metric_repo = mocker.Mock(spec=MetricRepo)
    mocker.patch.object(processor, '_add_configuration_data', return_value=metric_event)
    mocker.patch.object(processor, '_chose_storage_topic', return_value="test_topic")

    processor.send_to_downstream(metric_event, metric_repo)

    processor._add_configuration_data.assert_called_once_with(metric_event, metric_repo)
    processor._chose_storage_topic.assert_called_once_with(metric_event)
    metric_events_storage_session.save_event.assert_called_once_with(metric_event, "test_topic")


def test_add_configuration_data(processor, entities_storage_session, mocker):
    metric_event = mocker.Mock(spec=MetricEvent)
    metric_event.metric_uuid = UUID("00000000-0000-0000-0000-000000000000")
    metric_event.metric_group_id = None
    metric_event.metric_id = None
    metric_event.measure_frequency_id = None
    metric_entity = mocker.Mock()
    metric_group_entity = mocker.Mock()
    metric_repo = mocker.Mock(spec=MetricRepo)

    #todo: rewrite this test based on actual implementation

    # entities_storage_session.get_metric.return_value = metric_entity
    # entities_storage_session.get_metric_group.return_value = metric_group_entity
    #
    # result = processor._add_configuration_data(metric_event, metric_repo)
    #
    # entities_storage_session.get_metric.assert_called_once_with(metric_event.metric_uuid)
    # entities_storage_session.get_metric_group.assert_called_once_with(metric_entity.group_id)
    # assert result.metric_group_id == metric_group_entity.uuid
    # assert result.measure_frequency_id == metric_group_entity.measure_frequency_id


def test_chose_storage_topic_free_plan(processor, user, mocker):
    user.plan_id = Plan.FREE
    metric_event = mocker.Mock(spec=MetricEvent)
    metric_event.measure_frequency_id = MeasureFrequency.LOW_FREQUENCY

    topic = processor._chose_storage_topic(metric_event)
    assert topic == AbstractEventsStorage.TOPIC_FREE_PLAN_LOW_FREQ

    metric_event.measure_frequency_id = MeasureFrequency.MEDIUM_FREQUENCY
    topic = processor._chose_storage_topic(metric_event)
    assert topic == AbstractEventsStorage.TOPIC_FREE_PLAN_MEDIUM_FREQ

    metric_event.measure_frequency_id = MeasureFrequency.HIGH_FREQUENCY
    topic = processor._chose_storage_topic(metric_event)
    assert topic == AbstractEventsStorage.TOPIC_FREE_PLAN_HIGH_FREQ
