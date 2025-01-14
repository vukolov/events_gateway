import uuid
from sqlmodel import SQLModel, Field
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity


class MetricGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    name: str
    user_id: int
    measure_frequency_id: int
    active: bool

    def to_entity(self) -> MetricGroupEntity:
        return MetricGroupEntity(id=self.id,
                                 uuid=self.uuid,
                                 name=self.name,
                                 user_id=self.user_id,
                                 measure_frequency_id=self.measure_frequency_id,
                                 active=self.active)
