import argparse
import dotenv
import os
from infrastructure.interfaces.http.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.metric_events.kafka.kafka_producer import KafkaProducer
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env",
                        type=str,
                        choices=["dev", "test", "prod"],
                        help="Set the environment. By default is dev",
                        required=True, default="dev")
    args = parser.parse_args()
    dotenv.load_dotenv(f"configs/.env.{args.env}")

    downstream_metric_events_storage = KafkaProducer(os.getenv("DOWNSTREAM_KAFKA_BOOTSTRAP_SERVERS"))
    entities_storage = SqlEntitiesStorage(os.getenv("STORAGE_SQL_CONNECTION_STRING"))
    events_listener = EventsListener(downstream_metric_events_storage, entities_storage)
    events_listener.run()
