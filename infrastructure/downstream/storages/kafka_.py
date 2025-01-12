from entities.downstream.metrics.abstract_destination import AbstractDestination
from entities.storages.events_storage import EventsStorage
from kafka import KafkaProducer
import json


class Kafka(AbstractDestination, EventsStorage):
    def __init__(self, address: str):
        super().__init__(address)
        self._producer = KafkaProducer(
            bootstrap_servers=address,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def create_session(self):
        return self

    def close(self):
        self._producer.flush()
        self._producer.close()

    def send(self, message: dict, topic: str):
        self._producer.send(topic, value=message)
        # todo: is it necessary to flush every time?
        self._producer.flush()
