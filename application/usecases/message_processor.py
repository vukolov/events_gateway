from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.users.plan import Plan
from entities.metrics.metric_event import MetricEvent
from entities.metrics.measure_frequency import MeasureFrequency


class MessageProcessor:
    def __init__(self,
                 entities_storage_session: AbstractEntitiesStorageSession,
                 metric_events_storage_session: AbstractMetricEventsStorageSession,
                 user: UserEntity):
        self._entities_storage_session = entities_storage_session
        self._metric_events_storage_session = metric_events_storage_session
        self._user = user

    def process(self, metric_event: MetricEvent):
        metric_event = self._add_configuration_data(metric_event)
        topic = self._chose_storage_topic(metric_event)
        self._metric_events_storage_session.save_event(metric_event, topic)

    def _add_configuration_data(self, message: MetricEvent) -> MetricEvent:
        if not message.metric_group_uid or not message.measure_frequency_id:
            metric_entity = self._entities_storage_session.get_metric(message.metric_uid)
            metric_group_entity = self._entities_storage_session.get_metric_group(metric_entity.group_id)
            message.metric_group_uid = metric_group_entity.uuid
            message.measure_frequency_id = metric_group_entity.measure_frequency_id
        return message

    def _chose_storage_topic(self, message: MetricEvent) -> str:
        topic = None
        if self._user.plan_id == Plan.FREE:
            if message.measure_frequency_id == MeasureFrequency.LOW_FREQUENCY:
                topic = 'free_plan_low_freq'
            elif message.measure_frequency_id == MeasureFrequency.MEDIUM_FREQUENCY:
                topic = 'free_plan_medium_freq'
            elif message.measure_frequency_id == MeasureFrequency.HIGH_FREQUENCY:
                topic = 'free_plan_high_freq'
        return topic
