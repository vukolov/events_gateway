from infrastructure.upstream.api.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.kafka_ import Kafka
from infrastructure.downstream.storages.postgresql import Postgresql


if __name__ == "__main__":
    downstream_metrics_storage = Kafka("localhost:9092")
    users_storage = Postgresql()
    upstream = EventsListener(downstream_metrics_storage, users_storage)
    upstream.run()
