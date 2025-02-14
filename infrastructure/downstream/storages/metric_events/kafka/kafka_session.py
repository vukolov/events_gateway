from kafka import KafkaProducer as KafkaProducerLib
from entities.storage_sessions.abstract_metric_events_storage_session import AbstractMetricEventsStorageSession
from entities.metrics.metric_event import MetricEvent
from adapters.downstream.metric_event import MetricEvent as MetricEventDownstreamAdapter


class KafkaSession(AbstractMetricEventsStorageSession):
    def __init__(self, kafka_producer: KafkaProducerLib):
        self._kafka_producer = kafka_producer

    def get_session(self) -> KafkaProducerLib:
        return self._kafka_producer

    def save_event(self, event_data: MetricEvent, topic: str) -> None:
        prepared_metric_event = MetricEventDownstreamAdapter(event_data).to_dict()
        self._kafka_producer.send(topic, value=prepared_metric_event)
