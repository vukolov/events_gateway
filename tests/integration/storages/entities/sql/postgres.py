import dotenv
import os
from uuid import uuid4
from entities.metrics.metric import Metric
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage
from application.utils import *


#todo: create a new Neon.tech branch before the data manipulation

def test_add_metric():
    project_root = str(get_project_root())
    dotenv.load_dotenv(f"{project_root}/configs/.env.integration_tests")

    metric = Metric(uuid=uuid4(), name="integration_test_metric", active=False)

    entities_storage = SqlEntitiesStorage(os.getenv("STORAGE_SQL_CONNECTION_STRING"))
    with entities_storage.create_session() as session:
        metric_entity = session.add_metric(metric)
        assert metric_entity.id is not None
        assert metric_entity.uuid == metric.uuid
