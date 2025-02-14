from abc import ABCMeta
from application.storages.repositories.abstract_crud import AbstractCrud
from application.storages.repositories.abstract_repo import AbstractRepo


class MetricGroup(AbstractRepo, AbstractCrud, metaclass=ABCMeta):
    ...
