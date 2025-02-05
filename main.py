import dotenv
import os
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.metric_events.kafka.kafka_producer import KafkaProducer
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage


environment = os.getenv("ENV", "dev")
dotenv.load_dotenv(f"configs/.env.{environment}")

downstream_metric_events_storage = KafkaProducer(os.getenv("DOWNSTREAM_KAFKA_BOOTSTRAP_SERVERS"))
entities_storage = SqlEntitiesStorage(os.getenv("STORAGE_SQL_CONNECTION_STRING"))
events_listener = EventsListener(downstream_metric_events_storage, entities_storage)
app = events_listener.get_instance()

if __name__ == "__main__":
    events_listener.run()
