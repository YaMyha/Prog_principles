from abc import ABC, abstractmethod


class QueryBuilderBase(ABC):
    @property
    @abstractmethod
    def get_query(self) -> None:
        pass

    def match_filters(self, params: dict) -> None:
        print(params)
        for key, value in params.items():
            if value:
                self.arg_to_func.get(key)(value)
