from datetime import datetime


class MetricEvent:
    def __init__(self,
                 metric_group_uid: str | None,
                 metric_uid: str,
                 event_time: datetime,
                 metric_value: float,
                 measure_frequency_id: int | None):
        self.metric_group_uid = metric_group_uid
        self.metric_uid = metric_uid
        self.event_time = event_time
        self.metric_value = metric_value
        self.measure_frequency_id = measure_frequency_id
