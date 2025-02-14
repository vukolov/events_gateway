from uuid import UUID

from entities.abstract_business_entity import AbstractBusinessEntity


class MetricGroup(AbstractBusinessEntity):
    def __init__(self,
                 uuid: UUID,
                 name: str,
                 user_id: int,
                 measure_frequency_id: int,
                 active: bool,
                 id: int | None = None,):
        super().__init__(uuid=uuid, id=id)
        self.name = name
        self.user_id = user_id
        self.measure_frequency_id = measure_frequency_id
        self.active = active
