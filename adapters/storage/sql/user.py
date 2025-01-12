from sqlmodel import SQLModel
from entities.user import User as UserEntity


class User(SQLModel, table=True):
    username: str
    email: str
    full_name: str
    active: bool
    hashed_password: str

    def to_entity(self) -> UserEntity:
        return User(username=self.username,
                    email=self.email,
                    full_name=self.full_name,
                    active=self.active,
                    hashed_password=self.hashed_password)
