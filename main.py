from infrastructure.upstream.http.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.metric_events.kafka.kafka_producer import KafkaProducer
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage


if __name__ == "__main__":
    downstream_metrics_storage = KafkaProducer("localhost:9092")
    entities_storage = SqlEntitiesStorage("postgresql+psycopg2://user:password@localhost/dbname")
    upstream = EventsListener(downstream_metrics_storage, entities_storage)
    upstream.run()
