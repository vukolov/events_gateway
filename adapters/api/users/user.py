from pydantic import BaseModel
from entities.users.user import User as UserEntity


class User(BaseModel):
    id: int | None
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
