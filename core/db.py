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

CREATE TABLE IF NOT EXISTS confession_channel (
    guild_id   INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_response (
    input_text    TEXT PRIMARY KEY,
    response_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_allowed_user (
    user_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS wallet (
    user_id      INTEGER PRIMARY KEY,
    username     TEXT,
    coins        INTEGER NOT NULL DEFAULT 0,
    last_daily   INTEGER NOT NULL DEFAULT 0,
    last_weekly  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS anicat_user (
    user_id    INTEGER PRIMARY KEY,
    username   TEXT,
    total_cats INTEGER NOT NULL DEFAULT 0,
    total_pts  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS anicat_claim (
    user_id    INTEGER NOT NULL,
    card_name  TEXT NOT NULL,
    PRIMARY KEY (user_id, card_name)
);

CREATE TABLE IF NOT EXISTS message_count (
    user_id  INTEGER PRIMARY KEY,
    username TEXT,
    total    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reminder (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    due_at     INTEGER NOT NULL,
    message    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bot_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plays (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id   INTEGER NOT NULL,
    user_id    INTEGER,
    yt_id      TEXT NOT NULL,
    title      TEXT,
    source     TEXT NOT NULL DEFAULT 'user',
    played_at  INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_plays_guild ON plays(guild_id, played_at);

CREATE TABLE IF NOT EXISTS dj_settings (
    guild_id INTEGER PRIMARY KEY,
    dj_mode  INTEGER NOT NULL DEFAULT 0
);
"""

DEFAULT_PREFIX = "!"

_conn: aiosqlite.Connection | None = None
_prefix_cache: dict[int, str] = {}


def conn() -> aiosqlite.Connection:
    if _conn is None:
        raise RuntimeError("db not initialised; call init_db() first")
    return _conn


async def init_db() -> None:
    global _conn
    if _conn is not None:
        return
    _conn = await aiosqlite.connect(DB_PATH)
    await _conn.executescript(SCHEMA)
    await _conn.commit()


async def close_db() -> None:
    global _conn
    if _conn is None:
        return
    await _conn.close()
    _conn = None


async def get_prefix(guild_id: int) -> str:
    cached = _prefix_cache.get(guild_id)
    if cached is not None:
        return cached
    async with conn().execute(
        "SELECT prefix FROM guild_prefix WHERE guild_id = ?", (guild_id,)
    ) as cur:
        row = await cur.fetchone()
    prefix = row[0] if row else DEFAULT_PREFIX
    _prefix_cache[guild_id] = prefix
    return prefix


async def set_prefix(guild_id: int, prefix: str) -> None:
    await conn().execute(
        "INSERT INTO guild_prefix (guild_id, prefix) VALUES (?, ?) "
        "ON CONFLICT(guild_id) DO UPDATE SET prefix = excluded.prefix",
        (guild_id, prefix),
    )
    await conn().commit()
    _prefix_cache[guild_id] = prefix


async def delete_prefix(guild_id: int) -> None:
    await conn().execute("DELETE FROM guild_prefix WHERE guild_id = ?", (guild_id,))
    await conn().commit()
    _prefix_cache.pop(guild_id, None)


async def all_prefixes() -> dict[int, str]:
    async with conn().execute("SELECT guild_id, prefix FROM guild_prefix") as cur:
        rows = await cur.fetchall()
    return {row[0]: row[1] for row in rows}


async def get_meta(key: str) -> str | None:
    async with conn().execute(
        "SELECT value FROM bot_meta WHERE key = ?", (key,)
    ) as cur:
        row = await cur.fetchone()
    return row[0] if row else None


async def set_meta(key: str, value: str) -> None:
    await conn().execute(
        "INSERT INTO bot_meta (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )
    await conn().commit()


async def _get_channel(table: str, guild_id: int) -> int | None:
    async with conn().execute(
        f"SELECT channel_id FROM {table} WHERE guild_id = ?", (guild_id,)
    ) as cur:
        row = await cur.fetchone()
    return row[0] if row else None


async def _set_channel(table: str, guild_id: int, channel_id: int) -> None:
    await conn().execute(
        f"INSERT INTO {table} (guild_id, channel_id) VALUES (?, ?) "
        f"ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id",
        (guild_id, channel_id),
    )
    await conn().commit()


async def _delete_channel(table: str, guild_id: int) -> None:
    await conn().execute(f"DELETE FROM {table} WHERE guild_id = ?", (guild_id,))
    await conn().commit()


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


async def get_confession_channel(guild_id: int) -> int | None:
    return await _get_channel("confession_channel", guild_id)


async def set_confession_channel(guild_id: int, channel_id: int) -> None:
    await _set_channel("confession_channel", guild_id, channel_id)


async def delete_confession_channel(guild_id: int) -> None:
    await _delete_channel("confession_channel", guild_id)


async def set_chat_response(input_text: str, response_text: str) -> None:
    await conn().execute(
        "INSERT INTO chat_response (input_text, response_text) VALUES (?, ?) "
        "ON CONFLICT(input_text) DO UPDATE SET response_text = excluded.response_text",
        (input_text.lower(), response_text.lower()),
    )
    await conn().commit()


async def get_chat_response(input_text: str) -> str | None:
    async with conn().execute(
        "SELECT response_text FROM chat_response WHERE input_text = ?", (input_text.lower(),)
    ) as cur:
        row = await cur.fetchone()
    return row[0] if row else None


async def is_ai_allowed(user_id: int) -> bool:
    async with conn().execute(
        "SELECT 1 FROM ai_allowed_user WHERE user_id = ?", (user_id,)
    ) as cur:
        return (await cur.fetchone()) is not None


async def add_ai_allowed(user_id: int) -> None:
    await conn().execute("INSERT OR IGNORE INTO ai_allowed_user (user_id) VALUES (?)", (user_id,))
    await conn().commit()


async def wallet_exists(user_id: int) -> bool:
    async with conn().execute(
        "SELECT 1 FROM wallet WHERE user_id = ?", (user_id,)
    ) as cur:
        return (await cur.fetchone()) is not None


async def create_wallet(user_id: int, username: str) -> None:
    await conn().execute(
        "INSERT OR IGNORE INTO wallet (user_id, username, coins) VALUES (?, ?, 0)",
        (user_id, username),
    )
    await conn().commit()


async def get_wallet(user_id: int) -> dict | None:
    async with conn().execute(
        "SELECT user_id, username, coins, last_daily, last_weekly FROM wallet WHERE user_id = ?",
        (user_id,),
    ) as cur:
        row = await cur.fetchone()
    if not row:
        return None
    return {
        "user_id": row[0],
        "username": row[1],
        "coins": row[2],
        "last_daily": row[3],
        "last_weekly": row[4],
    }


async def update_coins(user_id: int, delta: int) -> None:
    await conn().execute(
        "UPDATE wallet SET coins = coins + ? WHERE user_id = ?", (delta, user_id)
    )
    await conn().commit()


async def claim_daily(user_id: int, now: int, amount: int) -> None:
    await conn().execute(
        "UPDATE wallet SET coins = coins + ?, last_daily = ? WHERE user_id = ?",
        (amount, now, user_id),
    )
    await conn().commit()


async def claim_weekly(user_id: int, now: int, amount: int) -> None:
    await conn().execute(
        "UPDATE wallet SET coins = coins + ?, last_weekly = ? WHERE user_id = ?",
        (amount, now, user_id),
    )
    await conn().commit()


async def transfer(sender_id: int, receiver_id: int, amount: int) -> None:
    db = conn()
    await db.execute("BEGIN")
    try:
        await db.execute(
            "UPDATE wallet SET coins = coins - ? WHERE user_id = ?", (amount, sender_id)
        )
        await db.execute(
            "UPDATE wallet SET coins = coins + ? WHERE user_id = ?", (amount, receiver_id)
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise


async def top_wallets(limit: int = 10) -> list[dict]:
    async with conn().execute(
        "SELECT username, coins FROM wallet ORDER BY coins DESC LIMIT ?", (limit,)
    ) as cur:
        rows = await cur.fetchall()
    return [{"username": r[0], "coins": r[1]} for r in rows]


async def record_anicat_claim(user_id: int, username: str, card_name: str, points: int) -> bool:
    """Record a card claim. Returns True if this was a new card for the user."""
    db = conn()
    await db.execute("BEGIN")
    try:
        await db.execute(
            "INSERT OR IGNORE INTO anicat_user (user_id, username) VALUES (?, ?)",
            (user_id, username),
        )
        cur = await db.execute(
            "INSERT OR IGNORE INTO anicat_claim (user_id, card_name) VALUES (?, ?)",
            (user_id, card_name),
        )
        is_new = cur.rowcount > 0
        await db.execute(
            "UPDATE anicat_user SET total_cats = total_cats + 1, total_pts = total_pts + ?, username = ? WHERE user_id = ?",
            (points, username, user_id),
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return is_new


async def get_anicat_user(user_id: int) -> dict | None:
    async with conn().execute(
        "SELECT user_id, username, total_cats, total_pts FROM anicat_user WHERE user_id = ?",
        (user_id,),
    ) as cur:
        row = await cur.fetchone()
    if not row:
        return None
    return {"user_id": row[0], "username": row[1], "total_cats": row[2], "total_pts": row[3]}


async def list_anicat_claims(user_id: int) -> list[str]:
    async with conn().execute(
        "SELECT card_name FROM anicat_claim WHERE user_id = ? ORDER BY card_name", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [r[0] for r in rows]


async def bump_message_count(user_id: int, username: str) -> int:
    """Increment message count for user. Returns new total."""
    db = conn()
    await db.execute(
        "INSERT INTO message_count (user_id, username, total) VALUES (?, ?, 1) "
        "ON CONFLICT(user_id) DO UPDATE SET total = total + 1, username = excluded.username",
        (user_id, username),
    )
    await db.commit()
    async with db.execute(
        "SELECT total FROM message_count WHERE user_id = ?", (user_id,)
    ) as cur:
        row = await cur.fetchone()
    return row[0]


async def get_message_count(user_id: int) -> int:
    async with conn().execute(
        "SELECT total FROM message_count WHERE user_id = ?", (user_id,)
    ) as cur:
        row = await cur.fetchone()
    return row[0] if row else 0


async def top_messages(limit: int = 10) -> list[dict]:
    async with conn().execute(
        "SELECT username, total FROM message_count ORDER BY total DESC LIMIT ?", (limit,)
    ) as cur:
        rows = await cur.fetchall()
    return [{"username": r[0], "total": r[1]} for r in rows]


async def record_play(
    guild_id: int, user_id: int | None, yt_id: str, title: str, source: str, now: int
) -> None:
    await conn().execute(
        "INSERT INTO plays (guild_id, user_id, yt_id, title, source, played_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (guild_id, user_id, yt_id, title, source, now),
    )
    await conn().commit()


async def recent_play_ids(guild_id: int, limit: int = 50) -> set[str]:
    """The most recently played YouTube ids in a guild, used to avoid repeats."""
    async with conn().execute(
        "SELECT yt_id FROM plays WHERE guild_id = ? ORDER BY played_at DESC LIMIT ?",
        (guild_id, limit),
    ) as cur:
        rows = await cur.fetchall()
    return {r[0] for r in rows}


async def get_dj_mode(guild_id: int) -> bool:
    async with conn().execute(
        "SELECT dj_mode FROM dj_settings WHERE guild_id = ?", (guild_id,)
    ) as cur:
        row = await cur.fetchone()
    return bool(row[0]) if row else False


async def set_dj_mode(guild_id: int, on: bool) -> None:
    await conn().execute(
        "INSERT INTO dj_settings (guild_id, dj_mode) VALUES (?, ?) "
        "ON CONFLICT(guild_id) DO UPDATE SET dj_mode = excluded.dj_mode",
        (guild_id, 1 if on else 0),
    )
    await conn().commit()


async def add_reminder(user_id: int, channel_id: int, due_at: int, message: str) -> int:
    db = conn()
    cur = await db.execute(
        "INSERT INTO reminder (user_id, channel_id, due_at, message) VALUES (?, ?, ?, ?)",
        (user_id, channel_id, due_at, message),
    )
    await db.commit()
    return cur.lastrowid


async def due_reminders(now: int) -> list[dict]:
    async with conn().execute(
        "SELECT id, user_id, channel_id, due_at, message FROM reminder WHERE due_at <= ?",
        (now,),
    ) as cur:
        rows = await cur.fetchall()
    return [
        {"id": r[0], "user_id": r[1], "channel_id": r[2], "due_at": r[3], "message": r[4]}
        for r in rows
    ]


async def delete_reminder(reminder_id: int) -> None:
    await conn().execute("DELETE FROM reminder WHERE id = ?", (reminder_id,))
    await conn().commit()


async def list_reminders(user_id: int) -> list[dict]:
    async with conn().execute(
        "SELECT id, due_at, message FROM reminder WHERE user_id = ? ORDER BY due_at",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [{"id": r[0], "due_at": r[1], "message": r[2]} for r in rows]
