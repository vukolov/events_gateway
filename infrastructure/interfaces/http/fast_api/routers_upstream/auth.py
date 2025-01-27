import os
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from ..jwt_encoder import JwtEncoder
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from application.usecases.auth import Auth
from application.exceptions.security.invalid_token import InvalidToken as InvalidTokenException
from adapters.api.users.token import Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
auth_usecase = Auth(JwtEncoder(os.getenv("UPSTREAM_SECURITY_TOKEN_SECRET"),
                               os.getenv("UPSTREAM_SECURITY_TOKEN_ALGORITHM")))


def init_auth_router(entities_storage: AbstractEntitiesStorage):
    router = APIRouter(
        prefix="/auth",
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    users_storage_session_dependency = Annotated[AbstractEntitiesStorageSession, Depends(entities_storage.create_session)]
    form_data_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

    @router.post("/token")
    async def token(users_storage_session: users_storage_session_dependency, form_data: form_data_dependency) -> Token:
        user = auth_usecase.authenticate_user(form_data.username, form_data.password, users_storage_session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth_usecase.create_access_token(user)
        return Token(access_token=access_token, token_type="bearer")
    return router


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           users_storage_session: Annotated[AbstractEntitiesStorageSession, Depends()]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = auth_usecase.get_user(token, users_storage_session)
    except InvalidTokenException:
        raise credentials_exception
    except Exception as e:
        raise e
    return user
