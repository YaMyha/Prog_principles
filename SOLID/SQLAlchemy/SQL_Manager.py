from contextlib import contextmanager
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SOLID.SQLAlchemy.DeclarativeBase import Base
from SOLID.Services import IrisService
from SOLID.config.Config_Manager import ConfigManager


def configure_engine():
    try:
        config_manager = ConfigManager()
        DATABASE = config_manager.get_config()
    except Exception as e:
        print("There was a problem loading the config.")
        print(e)
    try:
        return create_engine(URL.create(**DATABASE), echo=True)
    except Exception as e:
        print("There was a problem creating the engine.")
        print(e)


def create_session(engine):
    try:
        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine)
    except Exception as e:
        print("There was a problem creating the session.")
        print(e)


class SQLManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = configure_engine()
            cls._instance.Session = create_session(cls._instance.engine)
        return cls._instance

    @contextmanager
    def __create_session_scope(self):
        """Provides a transactional scope around a series of operations."""
        self.session = self.Session()
        try:
            yield self.session
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_irises(self):
        with self.__create_session_scope() as s:
            iris_service = IrisService(s)
            iris_service.get_irises()
