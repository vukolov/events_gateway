from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from entities.users.user import User as UserEntity
from adapters.storage.abstract_model import AbstractModel


class User(AbstractModel, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: UUID = Field(default_factory=uuid4, unique=True, index=True)
    username: str
    email: str
    full_name: str
    active: bool
    hashed_password: str
    plan_id: int

    def to_entity(self) -> UserEntity:
        return UserEntity(username=self.username,
                          email=self.email,
                          full_name=self.full_name,
                          active=self.active,
                          hashed_password=self.hashed_password,
                          plan_id=self.plan_id)

    @staticmethod
    def from_entity(entity: UserEntity) -> "User":
        return User(username=entity.username,
                    email=entity.email,
                    full_name=entity.full_name,
                    active=entity.active,
                    hashed_password=entity.hashed_password,
                    plan_id=entity.plan_id)
