import dotenv
from application.utils import *

project_root = str(get_project_root())
dotenv.load_dotenv(f"{project_root}/configs/.env.integration_tests")