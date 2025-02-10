from sqlmodel import Session, select
from uuid import UUID
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.clients.external_client import ExternalClient as ExternalClientEntity
from entities.metrics.metric import Metric as MetricEntity
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity
from adapters.storage.sql_models.user import User as UserModel
from adapters.storage.sql_models.external_client import ExternalClient as ExternalClientModel
from adapters.storage.sql_models.metric import Metric as MetricModel
from adapters.storage.sql_models.metric_group import MetricGroup as MetricGroupModel


class SqlEntitiesStorageSession(AbstractEntitiesStorageSession):
    def __init__(self, sqlmodel_session: Session):
        self._sqlmodel_session = sqlmodel_session

    def get_user(self, username: str) -> UserEntity:
        statement = select(UserModel).where(UserModel.username == username)
        return self._sqlmodel_session.exec(statement).one().to_entity()

    def get_external_client(self, client_uuid: UUID) -> ExternalClientEntity:
        statement = select(ExternalClientModel).where(ExternalClientModel.uuid == client_uuid)
        return self._sqlmodel_session.exec(statement).one().to_entity()

    def get_metric(self, metric_uuid: UUID) -> MetricEntity:
        statement = select(MetricModel).where(MetricModel.uuid == metric_uuid)
        return self._sqlmodel_session.exec(statement).one().to_entity()

    def add_metric(self, metric_entity: MetricEntity) -> MetricEntity:
        metric = MetricModel.from_entity(metric_entity)
        self._sqlmodel_session.add(metric)
        self._sqlmodel_session.flush()
        self._sqlmodel_session.refresh(metric)
        self._sqlmodel_session.commit()
        return metric.to_entity()

    def get_metric_group(self, group_id: int) -> MetricGroupEntity:
        statement = select(MetricGroupModel).where(MetricGroupModel.id == group_id)
        return self._sqlmodel_session.exec(statement).one().to_entity()
