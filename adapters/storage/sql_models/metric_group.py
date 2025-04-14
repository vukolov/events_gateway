from uuid import UUID, uuid4
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity
from adapters.storage.abstract_model import AbstractModel
from .table_names import METRIC_GROUPS

if TYPE_CHECKING:
    from adapters.storage.sql_models.metric import Metric


class MetricGroup(AbstractModel, SQLModel, table=True):

    __tablename__ = METRIC_GROUPS

    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str = Field(unique=True, index=True)
    user_id: int
    measure_frequency_id: int
    active: bool

    metrics: List["Metric"] = Relationship(back_populates="group", sa_relationship_kwargs={"lazy": "joined"})

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
