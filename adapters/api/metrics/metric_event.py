from pydantic import BaseModel, Field
from datetime import datetime


class MetricEvent(BaseModel):
    metric_group_uid: str
    metric_uid: str
    event_time: datetime
    metric_value: float
