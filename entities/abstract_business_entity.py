from abc import ABCMeta
from uuid import UUID


class AbstractBusinessEntity(metaclass=ABCMeta):
    def __init__(self,
                 uuid: UUID,
                 id: int | None = None):
        self.id = id
        self.uuid = uuid
