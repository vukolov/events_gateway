from typing import Generator
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from entities.storages.abstract_events_storage import AbstractEventsStorage
from infrastructure.downstream.storages.metric_events.file.file_session import FileSession


class FileStorage(AbstractEventsStorage):
    def __init__(self, address: str):
        Path(address).mkdir(parents=True, exist_ok=True)
        self._file_pointer = open(address + "/" + datetime.now().strftime("Y-m-d_H:M:S"), 'a')

    @contextmanager
    def create_session(self) -> Generator[FileSession, None, None]:
        yield FileSession(self._file_pointer)

    def close(self) -> None:
        self._file_pointer.close()
