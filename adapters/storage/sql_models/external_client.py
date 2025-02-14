from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from entities.clients.external_client import ExternalClient as ExternalClientEntity
from adapters.storage.abstract_model import AbstractModel


class ExternalClient(AbstractModel, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)

    def to_entity(self) -> ExternalClientEntity:
        return ExternalClientEntity(uuid=self.uuid)

    @staticmethod
    def from_entity(entity: ExternalClientEntity) -> "ExternalClient":
        return ExternalClient()
