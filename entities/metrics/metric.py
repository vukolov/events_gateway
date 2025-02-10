from uuid import UUID


class Metric:
    def __init__(self,
                 uuid: UUID,
                 name: str,
                 id: int | None = None,
                 group_id: int | None = None,
                 active: bool = False):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.group_id = group_id
        self.active = active
