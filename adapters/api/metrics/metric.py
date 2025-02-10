import uuid
from uuid import UUID
from pydantic import BaseModel
from entities.metrics.metric import Metric as MetricEntity


class MetricBase(BaseModel):
    id: int | None = None
    uuid: UUID | None = None
    name: str
    group_id: int | None = None
    active: bool = False

    def to_entity(self) -> MetricEntity:
        return MetricEntity(id=self.id,
                            uuid=self.uuid,
                            name=self.name,
                            group_id=self.group_id,
                            active=self.active)

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
    def from_entity(metric: MetricEntity):
        return MetricPublic(uuid=metric.uuid,
                            name=metric.name,
                            group_name='?',
                            active=metric.active)
