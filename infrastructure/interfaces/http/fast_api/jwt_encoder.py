import jwt
from jwt.exceptions import InvalidTokenError
from application.security.abstract_token_encoder import AbstractTokenEncoder
from application.exceptions.security.invalid_token import InvalidToken as InvalidTokenException


class JwtEncoder(AbstractTokenEncoder):
    def __init__(self, secret_key: str, algorithm: str):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, data: dict) -> str:
        return jwt.encode(data, self._secret_key, algorithm=self._algorithm)

    def decode(self, token: str) -> dict:
        try:
            data = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except InvalidTokenError:
            raise InvalidTokenException
        except Exception:
            raise
        return data
