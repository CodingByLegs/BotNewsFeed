import asyncio
import asyncpg

from data.config import PG_USER, PG_PASS, PG_IP


async def create_pool():
    return await asyncpg.create_pool(user=PG_USER,
                                     password=PG_PASS,
                                     host=PG_IP)



