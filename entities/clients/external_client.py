from uuid import UUID, uuid4
import secrets


class ExternalClient:
    def __init__(self,
                 id: int | None = None,
                 uuid: UUID | None = None):
        self.id: int | None = id
        self.uuid: UUID | None = uuid
        self.hashed_secret: str | None = None
        self.secret: str | None = None
        self.description: str | None = None
        if self.uuid is None:
            self.uuid = uuid4()
            self.secret = secrets.token_urlsafe(64)
