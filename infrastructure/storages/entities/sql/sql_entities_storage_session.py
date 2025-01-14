from sqlmodel import Session, select

from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User as UserEntity
from entities.metrics.metric import Metric as MetricEntity
from entities.metrics.metric_group import MetricGroup as MetricGroupEntity
from adapters.storage.sql_models.user import User as UserModel
from adapters.storage.sql_models.metric import Metric as MetricModel
from adapters.storage.sql_models.metric_group import MetricGroup as MetricGroupModel


class SqlEntitiesStorageSession(AbstractEntitiesStorageSession):
    def __init__(self, sqlmodel_session: Session):
        self._sqlmodel_session = sqlmodel_session

    def get_user(self, username: str) -> UserEntity:
        statement = select(UserModel).where(UserModel.username == username)
        return self._sqlmodel_session.exec(statement).one().to_entity()

    def get_metric(self, metric_uuid: str) -> MetricEntity:
        statement = select(MetricModel).where(MetricModel.uuid == uid)
        return self._sqlmodel_session.exec(statement).one().to_entity()

    def get_metric_group(self, group_id: int) -> MetricGroupEntity:
        statement = select(MetricGroupModel).where(MetricGroupModel.id == group_id)
        return self._sqlmodel_session.exec(statement).one().to_entity()
