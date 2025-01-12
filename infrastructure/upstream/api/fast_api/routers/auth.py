from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from application.usecases.auth import Auth
from adapters.api.users.token import Token
from entities.storage_sessions.abstract_users_storage_session import AbstractUsersStorageSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/auth",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                users_storage_session: Annotated[AbstractUsersStorageSession, Depends()]) -> Token:
    auth = Auth()
    user = auth.authenticate_user(form_data.username, form_data.password, users_storage_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           users_storage_session: Annotated[AbstractUsersStorageSession, Depends()]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = Auth().get_user(token, users_storage_session)
    except InvalidTokenError:
        raise credentials_exception
    except Exception as e:
        raise e
    return user
