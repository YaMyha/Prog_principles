import re

from sqlalchemy import select, and_

from db.modelsORM import Post, User
from db.services.query_builders.base_query_builder import QueryBuilderBase


class PostsQueryBuilder(QueryBuilderBase):
    def __init__(self) -> None:
        self._query = None
        self._components = None
        self.arg_to_func = {"author_name": self.filter_by_author, "tags": self.filter_by_tags}
        self.reset()

    def reset(self) -> None:
        self._query = select(Post).select_from(Post)
        self._components = []

    @property
    def get_query(self):
        query = self._query
        if self._components:
            query = query.filter(and_(*self._components))
        self.reset()
        return query

    def filter_by_author(self, author_name: str) -> None:
        """select *
            from posts
            where author_id in (
                select id
                from users
                where username like '%Steven%'
            );"""

        subquery = select(User.id).select_from(User).filter(User.username.contains(author_name))
        self._components.append(Post.author_id.in_(subquery))

    def filter_by_tags(self, tags: str) -> None:
        """select *
            from posts
            WHERE tags ~* '(?=.*(\W|^)secrets(\W|$))(?=.*(\W|^)men(\W|$)).*';"""
        tags = re.findall(r'\w+', tags)
        tags.append('.*')
        regex_pattern = ''.join(fr"(?=.*(\W|^){tag}(\W|$))" for tag in tags)

        self._components.append(Post.tags.regexp_match(regex_pattern.replace('\\\\', '\\')))
