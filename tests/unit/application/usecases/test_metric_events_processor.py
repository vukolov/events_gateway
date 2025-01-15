from uuid import UUID
from unittest import TestCase
from unittest.mock import MagicMock
from application.usecases.metric_events_processor import MetricEventsProcessor
from entities.storages.events_storage import AbstractEventsStorage
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.users.plan import Plan
from entities.metrics.metric_event import MetricEvent
from entities.metrics.measure_frequency import MeasureFrequency


class TestMetricEventsProcessor(TestCase):
    def setUp(self):
        self.entities_storage_session = MagicMock(spec=AbstractEntitiesStorageSession)
        self.metric_events_storage_session = MagicMock(spec=AbstractMetricEventsStorageSession)
        self.user = MagicMock(spec=UserEntity)
        self.processor = MetricEventsProcessor(self.entities_storage_session, self.metric_events_storage_session, self.user)

    def test_send_to_downstream(self):
        metric_event = MagicMock(spec=MetricEvent)
        self.processor._add_configuration_data = MagicMock(return_value=metric_event)
        self.processor._chose_storage_topic = MagicMock(return_value="test_topic")

        self.processor.send_to_downstream(metric_event)

        self.processor._add_configuration_data.assert_called_once_with(metric_event)
        self.processor._chose_storage_topic.assert_called_once_with(metric_event)
        self.metric_events_storage_session.save_event.assert_called_once_with(metric_event, "test_topic")

    def test_add_configuration_data(self):
        metric_event = MagicMock(spec=MetricEvent)
        metric_event.metric_uuid = UUID("00000000-0000-0000-0000-000000000000")
        metric_event.metric_group_id = None
        metric_event.metric_id = None
        metric_event.measure_frequency_id = None
        metric_entity = MagicMock()
        metric_group_entity = MagicMock()
        self.entities_storage_session.get_metric.return_value = metric_entity
        self.entities_storage_session.get_metric_group.return_value = metric_group_entity

        result = self.processor._add_configuration_data(metric_event)

        self.entities_storage_session.get_metric.assert_called_once_with(metric_event.metric_uuid)
        self.entities_storage_session.get_metric_group.assert_called_once_with(metric_entity.group_id)
        self.assertEqual(result.metric_group_id, metric_group_entity.uuid)
        self.assertEqual(result.measure_frequency_id, metric_group_entity.measure_frequency_id)

    def test_chose_storage_topic_free_plan(self):
        self.user.plan_id = Plan.FREE
        metric_event = MagicMock(spec=MetricEvent)
        metric_event.measure_frequency_id = MeasureFrequency.LOW_FREQUENCY

        topic = self.processor._chose_storage_topic(metric_event)

        self.assertEqual(topic, AbstractEventsStorage.TOPIC_FREE_PLAN_LOW_FREQ)

        metric_event.measure_frequency_id = MeasureFrequency.MEDIUM_FREQUENCY
        topic = self.processor._chose_storage_topic(metric_event)
        self.assertEqual(topic, AbstractEventsStorage.TOPIC_FREE_PLAN_MEDIUM_FREQ)

        metric_event.measure_frequency_id = MeasureFrequency.HIGH_FREQUENCY
        topic = self.processor._chose_storage_topic(metric_event)
        self.assertEqual(topic, AbstractEventsStorage.TOPIC_FREE_PLAN_HIGH_FREQ)