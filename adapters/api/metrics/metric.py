import uuid
from uuid import UUID
from pydantic import BaseModel
from entities.metrics.metric import Metric as MetricEntity


class MetricCreate(BaseModel):
    name: str

    def to_entity(self) -> MetricEntity:
        return MetricEntity(id=None,
                            uuid=uuid.uuid4(),
                            name=self.name,
                            group_id=None,
                            active=False)

class MetricPublic(BaseModel):
    uuid: UUID
    name: str
    group_name: str
    active: bool

    @staticmethod
    def from_entity(metric: MetricEntity) -> "MetricPublic":
        return MetricPublic(uuid=metric.uuid,
                            name=metric.name,
                            group_name='?',
                            active=metric.active)
