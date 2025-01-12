from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from entities.storages.users_storage import UsersStorage


class Postgresql(UsersStorage):
    def __init__(self):
        super().__init__()
        self._engine = create_engine("postgresql+psycopg2://user:password@localhost/dbname")
        self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        self._base = declarative_base()

    def create_session(self):
        session = self._session_maker()
        try:
            yield session
        finally:
            session.close()

    def close(self):
        ...
