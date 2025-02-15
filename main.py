import dotenv
import os

environment = os.getenv("ENV", "dev")
dotenv.load_dotenv(f"configs/.env.{environment}")

import importlib
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.metric_events.kafka.kafka_producer import KafkaProducer
from infrastructure.downstream.storages.metric_events.file.file_storage import FileStorage
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage


# downstream_metric_events_storage = KafkaProducer(os.getenv("DOWNSTREAM_KAFKA_BOOTSTRAP_SERVERS"))
downstream_metric_events_storage = FileStorage("/tmp/metric_events")
business_entities_storage = SqlEntitiesStorage(os.getenv("STORAGE_SQL_CONNECTION_STRING"))
entities_repos_path = "infrastructure.storages.entities.sql.repositories"
repos_module = importlib.import_module(entities_repos_path)
events_listener = EventsListener(downstream_metric_events_storage, business_entities_storage, repos_module)
app = events_listener.get_instance()

if __name__ == "__main__":
    events_listener.run()
