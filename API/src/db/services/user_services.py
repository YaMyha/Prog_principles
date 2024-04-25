from sqlalchemy import and_, select

from db.database import async_engine, async_session_factory
from db.modelsORM import User, Base


# Also pour try/catch sauce over it all
class UserService:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(username: str, hashed_password: str = None, email: str = None):
        async with async_session_factory() as session:
            user = User(username=username, hashed_password=hashed_password, email=email, rating=0)
            session.add(user)
            await session.flush()
            user_id = user.id
            await session.commit()
            return user_id

    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(User)
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
                select(User)
                .filter(and_(
                    User.rating > 0,
                    User.email.isnot(None)
                ))
            )
            result = await session.execute(query)
            users = result.scalars().all()
            print(users)
            return users

    @staticmethod
    async def update_user(uid: int, attrs: dict = None):
        async with async_session_factory() as session:
            user = await session.get(User, uid)
            if attrs:
                for key, value in attrs.items():
                    if value:
                        setattr(user, key, value)
                        await session.commit()

    @staticmethod
    async def delete_user(uid: int):
        async with async_session_factory() as session:
            user = await session.get(User, uid)
            session.delete(user)
            await session.commit()