# import asyncio
#
# from QueryManager import QueryManagerAsync
# from database import async_engine
#
#
# async def main():
#     await QueryManagerAsync.create_tables()
#     await QueryManagerAsync.insert_user(username='Steven', email='test@email.com', rating=10)
#     await QueryManagerAsync.insert_user(username='Michael', email='test@email.com', rating=10)
#     await QueryManagerAsync.insert_user(username='Selestina', rating=10)
#     await QueryManagerAsync.insert_user(username='Bully', rating=-10)
#     await QueryManagerAsync.insert_user(username='Steven Universe', rating=10)
#     await QueryManagerAsync.insert_post(author_id=1, title="Men's secrets", description="We have a beard!",
#                                         tags='secrets, men')
#     await QueryManagerAsync.insert_post(author_id=1, title="Men's secrets", description="We love potatoes with meat",
#                                         tags='secrets, men')
#     await QueryManagerAsync.insert_post(author_id=5, title="Men's secrets", description="Friendship is a magic!",
#                                         tags='secrets, men')
#     await QueryManagerAsync.insert_post(author_id=3, title="Women's secrets",
#                                         description="We can be angry if we're hungry",
#                                         tags='secrets, women')
#     await QueryManagerAsync.insert_post(author_id=4, title="Bully secrets", description="I don't bully anyone",
#                                         tags='secrets, bully')
#     # await QueryManagerAsync.select_posts_by_author('Steven')
#     await QueryManagerAsync.select_posts_by_tags(['bully'])
#     # await QueryManagerAsync.select_posts()
#     await async_engine.dispose()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
