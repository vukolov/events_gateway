from datetime import datetime
from uuid import UUID


class MetricEvent:
    def __init__(self,
                 metric_group_id: int | None,
                 metric_id: int | None,
                 metric_uuid: UUID,
                 event_time: datetime,
                 metric_value: float,
                 measure_frequency_id: int | None):
        self.metric_group_id = metric_group_id
        self.metric_id = metric_id
        self.metric_uuid = metric_uuid
        self.event_time = event_time
        self.metric_value = metric_value
        self.measure_frequency_id = measure_frequency_id
