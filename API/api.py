import asyncio

from QueryManager import QueryManagerAsync
from database import async_engine


async def main():
    await QueryManagerAsync.create_tables()
    await QueryManagerAsync.insert_user(username='Steven')
    await QueryManagerAsync.insert_user(username='Michael')
    await QueryManagerAsync.select_users()
    await QueryManagerAsync.update_user(uid=1, attrs={'username': 'Gabriel'})
    await QueryManagerAsync.select_users()
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
