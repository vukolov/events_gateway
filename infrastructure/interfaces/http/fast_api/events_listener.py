from fastapi import FastAPI, Depends
from entities.upstream.metrics.abstract_events_listener import AbstractEventsListener
from entities.storages.events_storage import AbstractEventsStorage
from entities.storages.abstract_entities_storage import AbstractEntitiesStorage
from .routers_upstream import auth
from .routers_upstream import metrics


class EventsListener(AbstractEventsListener):
    def __init__(self, events_storage: AbstractEventsStorage, entities_storage: AbstractEntitiesStorage):
        super().__init__(events_storage, entities_storage)
        app = FastAPI()

        app.include_router(auth.router, dependencies=[Depends(entities_storage.create_session)])
        app.include_router(metrics.router, dependencies=[
            Depends(entities_storage.create_session),
            Depends(events_storage.create_session)])

        @app.on_event("shutdown")
        async def shutdown_event():
            entities_storage.close()
            events_storage.close()

        self._app = app

    def run(self):
        ...
