import pdb

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, String
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import ARRAY

from database import Base, async_engine, async_session_factory
from modelsORM import UsersORM, PostsORM


# TO DO: Divide the functionality into several classes or consolidate it into a generic class
# Also pour try/catch sauce over it all
class QueryManagerAsync:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(username: str, password_hash: str = None, email: str = None):
        async with async_session_factory() as session:
            user = UsersORM(username=username, password_hash=password_hash, email=email, rating=0)
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
    async def select_users_with_positive_rating_and_filled_email():
        async with async_session_factory() as session:
            """select id, username, email, rating
                       from users
                       where rating > 0 and email is not NULL """
            query = (
                select(
                    UsersORM.id,
                    UsersORM.username,
                    UsersORM.password_hash,
                    UsersORM.email,
                    UsersORM.rating,
                    UsersORM.created_at,
                )
                .select_from(UsersORM)
                .filter(and_(
                    UsersORM.rating > 0,
                    UsersORM.email.isnot(None)
                ))
            )
            result = await session.execute(query)
            users = result.all()
            print(users)
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
    async def insert_post(author_id: int, title: str, description: str, tags: str = None):
        async with async_session_factory() as session:
            post = PostsORM(author_id=author_id, title=title, description=description, tags=tags)
            session.add(post)
            await session.flush()
            post_id = post.id
            await session.commit()
            return post_id

    @staticmethod
    async def select_posts():
        async with async_session_factory() as session:
            query = select(PostsORM)
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def select_posts_by_author(author_name: str):
        async with async_session_factory() as session:
            """select *
                from posts
                where author_id in (
                    select id 
                    from users
                    where username like '%Steven%'
                );"""
            subquery = select(UsersORM.id).select_from(UsersORM).filter(UsersORM.username.contains(author_name))
            query = select(PostsORM).select_from(PostsORM).filter(PostsORM.author_id.in_(subquery))

            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

    @staticmethod
    async def select_posts_by_tags(tags: list[str]):
        async with async_session_factory() as session:
            """select *
                from posts
                WHERE tags ~* '(?=.*(\W|^)secrets(\W|$))(?=.*(\W|^)men(\W|$)).*';"""
            tags.append('.*')
            regex_pattern = ''.join(fr"(?=.*(\W|^){tag}(\W|$))" for tag in tags)

            query = select(PostsORM).where(PostsORM.tags.regexp_match(regex_pattern.replace('\\\\', '\\')))
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
