import dotenv
import os
from uuid import uuid4
from entities.metrics.metric import Metric
from application.utils import *
from infrastructure.storages.entities.sql.sql_entities_storage import SqlEntitiesStorage
from infrastructure.storages.entities.sql.repositories.metric import Metric as MetricRepo


#todo: create a new Neon.tech branch before the data manipulation

def test_add_metric():
    project_root = str(get_project_root())
    dotenv.load_dotenv(f"{project_root}/configs/.env.integration_tests")

    metric = Metric(uuid=uuid4(), name="integration_test_metric", active=False)

    entities_storage = SqlEntitiesStorage(os.getenv("STORAGE_SQL_CONNECTION_STRING"))
    session = next(entities_storage.create_session())
    metric_repo = MetricRepo(session)
    metric_entity = metric_repo.add(metric)
    assert metric_entity.id is not None
    assert metric_entity.uuid == metric.uuid
