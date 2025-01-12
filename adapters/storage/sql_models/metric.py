import uuid
from sqlmodel import SQLModel, Field
from entities.metrics.metric import Metric as MetricEntity


class Metric(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: uuid.UUID = Field(default_factory=uuid.uuid4, index=True)
    name: str
    group_id: int
    active: bool

    def to_entity(self):
        return MetricEntity(id=self.id,
                            uuid=self.uuid,
                            name=self.name,
                            group_id=self.group_id,
                            active=self.active)
