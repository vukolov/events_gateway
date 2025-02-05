import os
from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Annotated
from infrastructure.interfaces.http.fast_api.jwt_encoder import JwtEncoder
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from entities.storage_sessions.abstract_entities_storage_session import AbstractEntitiesStorageSession
from application.usecases.auth import Auth
from application.exceptions.security.invalid_token import InvalidToken as InvalidTokenException
from adapters.api.users.token import Token


credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"})


def init_auth_router(entities_storage: AbstractEntitiesStorage) -> APIRouter:
    router = APIRouter(
        prefix="/v1/auth",
        responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    )

    auth_usecase = Auth(JwtEncoder(os.getenv("UPSTREAM_SECURITY_TOKEN_SECRET"),
                                   os.getenv("UPSTREAM_SECURITY_TOKEN_ALGORITHM")))

    users_storage_session_dependency = Annotated[AbstractEntitiesStorageSession, Depends(entities_storage.create_session)]

    @router.post("/token")
    async def generate_client_token(client_id: Annotated[str, Form()],
                                    client_secret: Annotated[str, Form()],
                                    users_storage_session: users_storage_session_dependency) -> Token:
        client = auth_usecase.authenticate_external_client(client_id, client_secret, users_storage_session)
        if not client:
            raise credentials_exception
        access_token = auth_usecase.create_client_access_token(client)
        return Token(access_token=access_token, token_type="bearer")

    @router.get("/grafana")
    async def authorize_client_and_redirect(client_id: str, redirect_uri: str, response_type: str):
        if response_type != "code":
            raise HTTPException(status_code=400, detail="Invalid response_type")
        code = "mock_code"
        return RedirectResponse(f"{redirect_uri}?code={code}")

    return router

oauth2_scheme_client = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")
async def get_current_client(token: Annotated[str, Depends(oauth2_scheme_client)],
                           clients_storage_session: Annotated[AbstractEntitiesStorageSession, Depends()]):
    try:
        auth_usecase = Auth(JwtEncoder(os.getenv("UPSTREAM_SECURITY_TOKEN_SECRET"),
                                       os.getenv("UPSTREAM_SECURITY_TOKEN_ALGORITHM")))
        client = auth_usecase.get_client(token, clients_storage_session)
    except InvalidTokenException:
        raise credentials_exception
    except Exception as e:
        raise e
    return client
