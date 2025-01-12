from pydantic import BaseModel
from datetime import datetime
from entities.metrics.metric_event import MetricEvent as MetricEventEntity
from adapters.storage.sql_models.metric import Metric as MetricModel


class MetricEvent(BaseModel):
    metric_uid: str
    event_time: datetime
    metric_value: float

    def to_entity(self) -> MetricEventEntity:
        return MetricEventEntity(
            metric_group_uid=None,
            metric_uid=self.metric_uid,
            event_time=self.event_time,
            metric_value=self.metric_value,
            measure_frequency_id=None,
        )
