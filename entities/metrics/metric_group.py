from uuid import UUID


class MetricGroup:
    def __init__(self, id: int, uuid: UUID, name: str, user_id: int, measure_frequency_id: int, active: bool):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.user_id = user_id
        self.measure_frequency_id = measure_frequency_id
        self.active = active
