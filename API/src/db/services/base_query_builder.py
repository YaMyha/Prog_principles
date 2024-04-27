from abc import ABC, abstractmethod


class QueryBuilderBase(ABC):
    @property
    @abstractmethod
    def get_query(self) -> None:
        pass

