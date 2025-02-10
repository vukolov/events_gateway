from typing import Generator, Any
from kafka import KafkaProducer as KafkaProducerLib
import json
from entities.storages.abstract_events_storage import AbstractEventsStorage
from infrastructure.downstream.storages.metric_events.kafka.kafka_session import KafkaSession


class KafkaProducer(AbstractEventsStorage):
    def __init__(self, address: str):
        self._producer = KafkaProducerLib(
            bootstrap_servers=address,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def create_session(self) -> Generator[KafkaSession, None, None]:
        yield KafkaSession(self._producer)

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()

    def send(self, message: dict[Any, Any], topic: str) -> None:
        self._producer.send(topic, value=message)
        # todo: is it necessary to flush every time?
        self._producer.flush()
