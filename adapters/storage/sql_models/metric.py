from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from entities.metrics.metric import Metric as MetricEntity
from adapters.storage.abstract_model import AbstractModel


class Metric(AbstractModel, SQLModel, table=True):

    __tablename__ = "metrics"

    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    group_id: int
    active: bool

    def to_entity(self) -> MetricEntity:
        return MetricEntity(id=self.id,
                            uuid=self.uuid,
                            name=self.name,
                            group_id=self.group_id,
                            active=self.active)

    @staticmethod
    def from_entity(metric: MetricEntity) -> "Metric":
        return Metric(id=metric.id,
                      uuid=metric.uuid,
                      name=metric.name,
                      group_id=metric.group_id,
                      active=metric.active)
