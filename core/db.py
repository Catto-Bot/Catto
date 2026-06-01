import aiosqlite

DB_PATH = "catto.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS guild_prefix (
    guild_id   INTEGER PRIMARY KEY,
    prefix     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS welcome_channel (
    guild_id   INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS leave_channel (
    guild_id   INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL
);
"""

DEFAULT_PREFIX = "!"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def get_prefix(guild_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db, db.execute(
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


async def _get_channel(table: str, guild_id: int) -> int | None:
    async with aiosqlite.connect(DB_PATH) as db, db.execute(
        f"SELECT channel_id FROM {table} WHERE guild_id = ?", (guild_id,)
    ) as cur:
        row = await cur.fetchone()
    return row[0] if row else None


async def _set_channel(table: str, guild_id: int, channel_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"INSERT INTO {table} (guild_id, channel_id) VALUES (?, ?) "
            f"ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id",
            (guild_id, channel_id),
        )
        await db.commit()


async def _delete_channel(table: str, guild_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"DELETE FROM {table} WHERE guild_id = ?", (guild_id,))
        await db.commit()


async def get_welcome_channel(guild_id: int) -> int | None:
    return await _get_channel("welcome_channel", guild_id)


async def set_welcome_channel(guild_id: int, channel_id: int) -> None:
    await _set_channel("welcome_channel", guild_id, channel_id)


async def delete_welcome_channel(guild_id: int) -> None:
    await _delete_channel("welcome_channel", guild_id)


async def get_leave_channel(guild_id: int) -> int | None:
    return await _get_channel("leave_channel", guild_id)


async def set_leave_channel(guild_id: int, channel_id: int) -> None:
    await _set_channel("leave_channel", guild_id, channel_id)


async def delete_leave_channel(guild_id: int) -> None:
    await _delete_channel("leave_channel", guild_id)
