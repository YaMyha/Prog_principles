from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import Base, async_engine, async_session_factory
from modelsORM import UsersORM, PostsORM


# TO DO: Divide the functionality into several classes or consolidate it into a generic class
class QueryManagerAsync:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(username: str, password_hash: str = None, email: str = None):
        async with async_session_factory() as session:
            user = UsersORM(username=username, password_hash=password_hash, email=email)
            session.add(user)
            await session.flush()
            user_id = user.id
            await session.commit()
            return user_id

    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(UsersORM)
            result = await session.execute(query)
            users = result.scalars().all()
            return users

    @staticmethod
    async def update_user(uid: int, attrs: dict = None):
        async with async_session_factory() as session:
            user = await session.get(UsersORM, uid)
            if attrs:
                for key, value in attrs.items():
                    if key:
                        setattr(user, key, value)
                        await session.commit()

    @staticmethod
    async def delete_user(uid: int):
        async with async_session_factory() as session:
            user = await session.get(UsersORM, uid)
            session.delete(user)
            await session.commit()

    @staticmethod
    async def insert_post(author_id: int, title: str, description: str):
        async with async_session_factory() as session:
            post = PostsORM(author_id=author_id, title=title, description=description)
            session.add(post)
            await session.flush()
            post_id = post.id
            await session.commit()
            return post.id

    @staticmethod
    async def select_posts():
        async with async_session_factory() as session:
            query = select(PostsORM)
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def update_post(post_id: int, attrs: dict = None):
        async with async_session_factory() as session:
            post = await session.get(PostsORM, post_id)
            if attrs:
                for key, value in attrs.items():
                    if key:
                        setattr(post, key, value)
                        await session.commit()

    @staticmethod
    async def delete_post(uid: int):
        async with async_session_factory() as session:
            post = await session.get(PostsORM, uid)
            session.delete(post)
            await session.commit()
