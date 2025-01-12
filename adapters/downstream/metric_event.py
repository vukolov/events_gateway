from entities.metrics.metric_event import MetricEvent as MetricEventEntity


class MetricEvent:
    def __init__(self, metric_event_entity: MetricEventEntity):
        self.metric_group_uid = metric_event_entity.metric_group_uid
        self.metric_uid = metric_event_entity.metric_uid
        self.event_time = metric_event_entity.event_time
        self.metric_value = metric_event_entity.metric_value

    def to_dict(self):
        return {
            "metric_group_uid": self.metric_group_uid,
            "metric_uid": self.metric_uid,
            "event_time": self.event_time,
            "metric_value": self.metric_value
        }
