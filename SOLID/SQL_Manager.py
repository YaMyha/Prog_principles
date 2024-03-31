from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from Config_Manager import ConfigManager
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DeclarativeBase(Base):
    __abstract__ = True


class SQLManager:
    def __init__(self):
        self.engine = None
        self.session = None
        self.__create_engine()
        self.__create_session()
        self.post_manager = PostManager(self.session)

    def __create_engine(self):
        config_manager = ConfigManager()
        DATABASE = config_manager.get_config()
        self.engine = create_engine(URL.create(**DATABASE))

    def __create_session(self):
        DeclarativeBase.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class Post(DeclarativeBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    url = Column('url', String)

    def __repr__(self):
        return f"Post {self.name}: {self.url}"


class PostManager:

    def __init__(self, session):
        self.session = session

    def add_post(self):
        new_post = Post(name='Two record', url="http://testsite.ru/first_record")
        self.session.add(new_post)

        for post in self.session.query(Post):
            print(post)
