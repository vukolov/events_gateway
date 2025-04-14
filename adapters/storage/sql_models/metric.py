from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from entities.metrics.metric import Metric as MetricEntity
from adapters.storage.abstract_model import AbstractModel
from .table_names import METRICS, METRIC_GROUPS

if TYPE_CHECKING:
    from adapters.storage.sql_models.metric_group import MetricGroup


class Metric(AbstractModel, SQLModel, table=True):

    __tablename__ = METRICS

    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    name: str
    group_id: int = Field(foreign_key=f"{METRIC_GROUPS}.id")
    active: bool
    group: Optional["MetricGroup"] = Relationship(back_populates=METRICS)

    def to_entity(self) -> MetricEntity:
        return MetricEntity(id=self.id,
                            uuid=self.uuid,
                            name=self.name,
                            group_id=self.group_id,
                            group_name=self.group.name if self.group else None,
                            active=self.active)

    @staticmethod
    def from_entity(metric: MetricEntity) -> "Metric":
        return Metric(id=metric.id,
                      uuid=metric.uuid,
                      name=metric.name,
                      group_id=metric.group_id,
                      active=metric.active)
