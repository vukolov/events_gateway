import pytest
from application.usecases.auth import Auth
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from application.security.abstract_token_encoder import AbstractTokenEncoder
from application.exceptions.security.invalid_token import InvalidToken as InvalidTokenException
from entities.users.user import User


@pytest.fixture
def users_storage_session(mocker):
    mock = mocker.Mock(spec=AbstractEntitiesStorageSession)

    def get_user_side_effect(user_name):
        if user_name == 'test_user':
            user = User()
            user.username = user_name
            user.hashed_password = Auth.hash_password("correct_password")
            return user
        else:
            return None

    mock.get_user.side_effect = get_user_side_effect
    return mock


@pytest.fixture
def token_encoder(mocker):
    mock = mocker.Mock(spec=AbstractTokenEncoder)

    def encode_side_effect(to_encode: dict):
        return to_encode['sub'] + "_token"

    def decode_side_effect(token: str):
        if token == "invalid_token":
            raise InvalidTokenException("Invalid token")
        return {"sub": token.replace("_token", "")}

    mock.encode.side_effect = encode_side_effect
    mock.decode.side_effect = decode_side_effect
    return mock


def test_authenticate_user(users_storage_session, token_encoder, mocker):
    auth = Auth(token_encoder)
    assert auth.authenticate_user("not_existed_user", "", users_storage_session) is False
    assert auth.authenticate_user("test_user", "wrong_password", users_storage_session) is False
    user = auth.authenticate_user("test_user", "correct_password", users_storage_session)
    assert isinstance(user, User)
    assert user.username == "test_user"


def test_create_access_token(token_encoder):
    auth = Auth(token_encoder)
    user = User()
    user.username = "test_user"
    token = auth.create_access_token(user)
    assert token == "test_user_token"


def test_get_user(users_storage_session, token_encoder):
    auth = Auth(token_encoder)
    with pytest.raises(InvalidTokenException) as e:
        auth.get_user("invalid_token", users_storage_session)
    user = auth.get_user("test_user_token", users_storage_session)
    assert isinstance(user, User)
    assert user.username == "test_user"
