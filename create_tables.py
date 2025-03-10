import asyncio
from db_setup import engine, Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        ## тут треба асинхронно створити таблиці


if __name__ == "__main__":
    asyncio.run(create_tables())
