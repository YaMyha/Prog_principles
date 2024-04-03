from abc import ABC

from SOLID.SQLAlchemy.Iris import Iris


class ServiceBase(ABC):

    def __init__(self, session):
        self.session = session


class IrisService(ServiceBase):

    def get_irises(self):
        irises = self.session.query(Iris).filter(
            Iris.sepallengthcm == 5.1,
        ).order_by(Iris.id.desc()).limit(10).all()
        for iris in irises:
            print(iris)
