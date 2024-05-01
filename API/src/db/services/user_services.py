from db.database import async_session_factory
from db.modelsORM import User
from db.services.query_builders.users_query_builder import UsersQueryBuilder


# Also pour try/catch sauce over it all
class UserService:
    def __init__(self):
        self.users_query_builder = UsersQueryBuilder()

    @staticmethod
    async def insert_user(username: str, hashed_password: str, email: str = None):
        async with async_session_factory() as session:
            user = User(username=username, hashed_password=hashed_password, email=email, rating=0)
            session.add(user)
            await session.flush()
            user_id = user.id
            await session.commit()
            return user_id

    async def select_posts(self, parameters: dict):
        async with async_session_factory() as session:
            self.users_query_builder.match_filters(parameters)
            query = self.users_query_builder.get_query
            result = await session.execute(query)
            posts = result.scalars().all()
            return posts

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
            if user:
                await session.delete(user)
                await session.commit()
