import asyncio
import aiosqlite

Db_path = "logging.db"

async def async_fetch_users():
    async with aiosqlite.connect(Db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print(f"Fetched {len(rows)} users:")
            for row in rows:
                print(row)

async def async_fetch_older_users():
    async with aiosqlite.connect(Db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print(f"Fetched {len(rows)} users over 40:")
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
    print("All queries executed concurrently.")
