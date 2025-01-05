from .abstract_storage import AbstractStorage
from entities.user import User


class UsersStorage(AbstractStorage):
    def get_user(self, username: str) -> User:
        ...
