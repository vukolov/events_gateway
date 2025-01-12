from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from entities.users.user import User


class Auth:
    SECRET_KEY = "49b76e094faa6ca2556c818166b7a2244b93f7099f6f0f4caa6cf63b88e8d3e2"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def authenticate_user(self, username: str, password: str, users_storage_session: AbstractEntitiesStorageSession) -> User | bool:
        user = users_storage_session.get_user(username)
        if user is None:
            return False
        if not self._pwd_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Auth.SECRET_KEY, algorithm=Auth.ALGORITHM)
        return encoded_jwt

    def get_user(self, token: str, users_storage_session: AbstractEntitiesStorageSession) -> User:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Could not validate credentials")
        user = users_storage_session.get_user(username)
        if user is None:
            raise Exception("No such user")
        return user
