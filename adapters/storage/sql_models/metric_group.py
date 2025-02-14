from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity
from adapters.storage.abstract_model import AbstractModel


class MetricGroup(AbstractModel, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
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

    @staticmethod
    def from_entity(entity: MetricGroupEntity) -> "MetricGroup":
        return MetricGroup(id=entity.id,
                           uuid=entity.uuid,
                           name=entity.name,
                           user_id=entity.user_id,
                           measure_frequency_id=entity.measure_frequency_id,
                           active=entity.active)
