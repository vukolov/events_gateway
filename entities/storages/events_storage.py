from abc import ABCMeta, abstractmethod
from entities.storages.abstract_storage import AbstractStorage


class AbstractEventsStorage(AbstractStorage, metaclass=ABCMeta):
    TOPIC_FREE_PLAN_LOW_FREQ = 'free_plan_low_freq'
    TOPIC_FREE_PLAN_MEDIUM_FREQ = 'free_plan_medium_freq'
    TOPIC_FREE_PLAN_HIGH_FREQ = 'free_plan_high_freq'
