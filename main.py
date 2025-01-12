from infrastructure.upstream.api.fast_api.events_listener import EventsListener
from infrastructure.downstream.storages.kafka_ import Kafka
from infrastructure.storages.users.sql.sql_users_storage import SqlUsersStorage


if __name__ == "__main__":
    downstream_metrics_storage = Kafka("localhost:9092")
    users_storage = SqlUsersStorage("postgresql+psycopg2://user:password@localhost/dbname")
    upstream = EventsListener(downstream_metrics_storage, users_storage)
    upstream.run()
