from typing import TextIO
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.metrics.metric_event import MetricEvent
from adapters.downstream.metric_event import MetricEvent as MetricEventDownstreamAdapter


class FileSession(AbstractMetricEventsStorageSession):
    def __init__(self, file_pointer: TextIO):
        self._file_pointer = file_pointer

    def get_session(self) -> TextIO:
        return self._file_pointer

    def save_event(self, event_data: MetricEvent, topic: str) -> None:
        prepared_metric_event = MetricEventDownstreamAdapter(event_data).to_dict()
        self._file_pointer.write(f"{topic}: {prepared_metric_event}\n")
