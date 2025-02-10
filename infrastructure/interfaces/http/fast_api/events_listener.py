from fastapi import FastAPI
from contextlib import asynccontextmanager
from entities.upstream.metrics.abstract_events_listener import AbstractEventsListener
from entities.storages.abstract_events_storage import AbstractEventsStorage
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from infrastructure.interfaces.http.fast_api.routers_upstream.v1.events import init_events_router
from infrastructure.interfaces.http.fast_api.routers_common.v1.auth import init_auth_router, TokenChecker
from infrastructure.interfaces.http.fast_api.routers_config.v1.metrics import init_metrics_router


class EventsListener(AbstractEventsListener):
    def __init__(self, events_storage: AbstractEventsStorage, entities_storage: AbstractEntitiesStorage):
        super().__init__(events_storage, entities_storage)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            entities_storage.close()
            events_storage.close()

        token_checker = TokenChecker(entities_storage)

        app = FastAPI(lifespan=lifespan)
        app.include_router(init_auth_router(entities_storage))
        app.include_router(init_metrics_router(token_checker))
        app.include_router(init_events_router(token_checker, events_storage))
        self._app = app

    def run(self) -> None:
        ...

    def get_instance(self) -> FastAPI:
        return self._app
