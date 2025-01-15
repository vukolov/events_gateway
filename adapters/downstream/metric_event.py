from entities.metrics.metric_event import MetricEvent as MetricEventEntity


class MetricEvent:
    def __init__(self, metric_event_entity: MetricEventEntity):
        self._metric_event_entity = metric_event_entity

    def to_dict(self):
        return {
            "metric_group_id": self._metric_event_entity.metric_group_id,
            "metric_id": self._metric_event_entity.metric_id,
            "event_time": self._metric_event_entity.event_time,
            "metric_value": self._metric_event_entity.event_time
        }
