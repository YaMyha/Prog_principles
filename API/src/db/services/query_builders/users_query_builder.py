from sqlalchemy import select, and_

from db.modelsORM import User
from db.services.query_builders.base_query_builder import QueryBuilderBase


class UsersQueryBuilder(QueryBuilderBase):
    def __init__(self) -> None:
        self._query = None
        self._components = None
        self.arg_to_func = {"user_id": self.filter_by_id,
                            "rating_bottom": self.filter_by_rating_bottom, "rating_top": self.filter_by_rating_top}
        self.reset()

    def reset(self) -> None:
        self._query = select(User).select_from(User)
        self._components = []

    @property
    def get_query(self):
        """select id, username, email, rating
                                   from users
                                   where rating > 0 and email is not NULL for example"""
        query = self._query
        if self._components:
            query = query.filter(and_(*self._components))
        self.reset()
        return query

    def filter_by_id(self, user_id: int):
        if user_id:
            self._components.append(User.id == user_id)

    def filter_by_rating_top(self, range_top: int) -> None:
        if range_top:
            self._components.append(User.rating <= range_top)

    def filter_by_rating_bottom(self, range_bottom: int) -> None:
        if range_bottom:
            self._components.append(User.rating >= range_bottom)
