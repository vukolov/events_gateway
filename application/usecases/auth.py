from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from application.security.abstract_token_encoder import AbstractTokenEncoder
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User


class Auth:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, token_encoder: AbstractTokenEncoder):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._token_encoder = token_encoder

    def authenticate_user(self, username: str, password: str, users_storage_session: AbstractEntitiesStorageSession) -> User | bool:
        user = users_storage_session.get_user(username)
        if user is None:
            return False
        if not self._pwd_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, user: User) -> str:
        to_encode = {
            "sub": user.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return self._token_encoder.encode(to_encode)

    def get_user(self, token: str, users_storage_session: AbstractEntitiesStorageSession) -> User:
        payload = self._token_encoder.decode(token)
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Could not validate credentials")
        user = users_storage_session.get_user(username)
        if user is None:
            raise Exception("No such user")
        return user
