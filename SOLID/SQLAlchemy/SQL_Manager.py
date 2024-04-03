from contextlib import contextmanager
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SOLID.SQLAlchemy.DeclarativeBase import Base
from SOLID.Services import IrisService
from SOLID.config.Config_Manager import ConfigManager


class SQLManager:
    def __init__(self):
        self.engine = None
        self.session = None
        self.__create_engine()
        self.__create_session()

    def __create_engine(self):
        config_manager = ConfigManager()
        DATABASE = config_manager.get_config()
        self.engine = create_engine(URL.create(**DATABASE), echo=True)

    def __create_session(self):
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        """Provides a transactional scope around a series of operations."""
        self.session = self.DBSession()
        try:
            yield self.session
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_irises(self):
        with self.session_scope() as s:
            post_service = IrisService(s)
            post_service.get_irises()
