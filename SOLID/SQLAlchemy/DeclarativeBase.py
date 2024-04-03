from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DeclarativeBase(Base):
    __abstract__ = True
