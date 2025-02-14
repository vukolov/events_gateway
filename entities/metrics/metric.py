from uuid import UUID

from entities.abstract_business_entity import AbstractBusinessEntity


class Metric(AbstractBusinessEntity):
    def __init__(self,
                 uuid: UUID,
                 name: str,
                 id: int | None = None,
                 group_id: int | None = None,
                 active: bool = False):
        super().__init__(uuid=uuid, id=id)
        self.name = name
        self.group_id = group_id
        self.active = active
