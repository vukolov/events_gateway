from uuid import UUID, uuid4
import secrets
from entities.abstract_business_entity import AbstractBusinessEntity


class ExternalClient(AbstractBusinessEntity):
    def __init__(self,
                 uuid: UUID,
                 id: int | None = None):
        super().__init__(uuid=uuid, id=id)
        self.hashed_secret: str | None = None
        self.secret: str | None = None
        self.description: str | None = None
        if self.uuid is None:
            self.uuid = uuid4()
            self.secret = secrets.token_urlsafe(64)
