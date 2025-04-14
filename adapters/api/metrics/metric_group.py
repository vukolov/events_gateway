import uuid
from uuid import UUID
from pydantic import BaseModel
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity


class MetricGroupCreate(BaseModel):
    name: str

    def to_entity(self) -> MetricGroupEntity:
        return MetricGroupEntity(uuid=uuid.uuid4(),
                                 name=self.name,
                                 user_id=0,
                                 measure_frequency_id=0,
                                 active=True,
                                 id=None,
                                 )


class MetricGroupPublic(BaseModel):
    uuid: UUID
    name: str
    group_name: str
    active: bool

    @staticmethod
    def from_entity(metric: MetricGroupEntity) -> "MetricGroupPublic":
        return MetricGroupPublic(uuid=metric.uuid,
                                 name=metric.name,
                                 group_name='?',
                                 active=metric.active)
