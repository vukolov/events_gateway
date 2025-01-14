from sqlmodel import SQLModel
from entities.users.user import User as UserEntity


class Plan(SQLModel, table=True):
    id: int
    name: str
    description: str

    def to_entity(self) -> UserEntity:
        ...
