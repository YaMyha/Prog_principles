from db.database import async_session_factory
from db.modelsORM import Post
from db.services.query_builders.posts_query_builder import PostsQueryBuilder


class PostService:
    def __init__(self):
        self.posts_query_builder = PostsQueryBuilder()

    @staticmethod
    async def insert_post(author_id: int, title: str, description: str, tags: str = None):
        async with async_session_factory() as session:
            post = Post(author_id=author_id, title=title, description=description, tags=tags)
            session.add(post)
            await session.flush()
            post_id = post.id
            await session.commit()
            return post_id

    async def select_posts(self, parameters: dict):
        async with async_session_factory() as session:
            self.posts_query_builder.match_filters(parameters)
            query = self.posts_query_builder.get_query
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def update_post(post_id: int, attrs: dict = None):
        async with async_session_factory() as session:
            post = await session.get(Post, post_id)
            if attrs:
                for key, value in attrs.items():
                    if key:
                        setattr(post, key, value)
                        await session.commit()

    @staticmethod
    async def delete_post(post_id: int):
        async with async_session_factory() as session:
            post = await session.get(Post, post_id)
            if post:
                await session.delete(post)
                await session.commit()
