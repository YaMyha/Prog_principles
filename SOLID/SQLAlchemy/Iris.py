from SOLID.SQLAlchemy.DeclarativeBase import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, SmallInteger


class Iris(DeclarativeBase):
    __tablename__ = 'iris'

    id = Column('id', SmallInteger, primary_key=True)
    sepallengthcm = Column('sepallengthcm', Float)
    sepalwidthcm = Column('sepalwidthcm', Float)
    petallengthcm = Column('petallengthcm', Float)
    petalwidthcm = Column('petalwidthcm', Float)
    species = Column('species', String)

    def __repr__(self):
        return f"Iris {self.id}: {self.species}"


