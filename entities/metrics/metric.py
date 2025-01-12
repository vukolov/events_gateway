from uuid import UUID


class Metric:
    def __init__(self, id: int, uuid: UUID, name: str, group_id: int, active: bool):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.group_id = group_id
        self.active = active
