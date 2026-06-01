import aiosqlite

DB_PATH = "catto.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS guild_prefix (
    guild_id   INTEGER PRIMARY KEY,
    prefix     TEXT NOT NULL
);
"""

DEFAULT_PREFIX = "!"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def get_prefix(guild_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT prefix FROM guild_prefix WHERE guild_id = ?", (guild_id,)
        ) as cur:
            row = await cur.fetchone()
    return row[0] if row else DEFAULT_PREFIX


async def set_prefix(guild_id: int, prefix: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO guild_prefix (guild_id, prefix) VALUES (?, ?) "
            "ON CONFLICT(guild_id) DO UPDATE SET prefix = excluded.prefix",
            (guild_id, prefix),
        )
        await db.commit()


async def delete_prefix(guild_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM guild_prefix WHERE guild_id = ?", (guild_id,))
        await db.commit()
