from asyncpg import create_pool

async def db_config():
   return await create_pool(min_size=2, max_size=2, max_queries=50000,
                         host='jipdb.ctcgmkl18wuj.ap-northeast-2.rds.amazonaws.com',
                         user='jip', password='35343534', database='love_story')