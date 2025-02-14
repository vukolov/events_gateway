from uuid import UUID, uuid4
from entities.abstract_business_entity import AbstractBusinessEntity


class User(AbstractBusinessEntity):
    def __init__(self,
                 uuid: UUID = uuid4(),
                 id: int | None = None,
                 username: str | None = None,
                 email: str | None = None,
                 full_name: str | None = None,
                 active: bool = True,
                 hashed_password: str | None = None,
                 plan_id: int | None = None):
        super().__init__(uuid=uuid, id=id)
        self.username: str | None = None
        self.email: str | None = None
        self.full_name: str | None = None
        self.active: bool = True
        self.hashed_password: str | None = None
        self.plan_id: int | None = None
