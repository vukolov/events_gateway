from sqlmodel import SQLModel, Field
from entities.users.user import User as UserEntity


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    full_name: str
    active: bool
    hashed_password: str
    plan_id: int

    def to_entity(self) -> UserEntity:
        return User(username=self.username,
                    email=self.email,
                    full_name=self.full_name,
                    active=self.active,
                    hashed_password=self.hashed_password)
