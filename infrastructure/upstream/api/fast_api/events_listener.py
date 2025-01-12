from fastapi import FastAPI, Depends
from entities.upstream.metrics.abstract_events_listener import AbstractEventsListener
from entities.storages.events_storage import EventsStorage
from entities.storages.abstract_users_storage import AbstractUsersStorage
from .routers import auth
from .routers import metrics


class EventsListener(AbstractEventsListener):
    def __init__(self, events_storage: EventsStorage, users_storage: AbstractUsersStorage):
        super().__init__(events_storage, users_storage)
        app = FastAPI()

        app.include_router(auth.router, dependencies=[Depends(users_storage.create_session)])
        app.include_router(metrics.router, dependencies=[Depends(events_storage.create_session)])

        @app.on_event("shutdown")
        async def shutdown_event():
            events_storage.close()

        self._app = app

    def run(self):
        ...
