from sqlmodel import SQLModel, Field
from entities.clients.external_client import ExternalClient as ExternalClientEntity


class ExternalClient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    def to_entity(self) -> ExternalClientEntity:
        return ExternalClientEntity()
