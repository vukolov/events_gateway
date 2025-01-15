from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from entities.metrics.metric_event import MetricEvent as MetricEventEntity


class MetricEvent(BaseModel):
    metric_uuid: UUID
    event_time: datetime
    metric_value: float

    def to_entity(self) -> MetricEventEntity:
        return MetricEventEntity(
            metric_group_id=None,
            metric_uuid=self.metric_uuid,
            event_time=self.event_time,
            metric_value=self.metric_value,
            measure_frequency_id=None,
        )
