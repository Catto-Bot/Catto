from core import db


async def test_prefix_defaults_to_bang():
    assert await db.get_prefix(123) == "!"


async def test_set_and_get_prefix():
    await db.set_prefix(123, "?")
    assert await db.get_prefix(123) == "?"


async def test_set_prefix_overwrites():
    await db.set_prefix(123, "?")
    await db.set_prefix(123, "$")
    assert await db.get_prefix(123) == "$"


async def test_delete_prefix_returns_to_default():
    await db.set_prefix(123, "?")
    await db.delete_prefix(123)
    assert await db.get_prefix(123) == db.DEFAULT_PREFIX


async def test_prefix_cache_populated_after_lookup():
    await db.set_prefix(1, "?")
    db._prefix_cache.clear()
    await db.get_prefix(1)
    assert db._prefix_cache[1] == "?"


async def test_prefix_cache_invalidated_by_delete():
    await db.set_prefix(1, "?")
    assert db._prefix_cache[1] == "?"
    await db.delete_prefix(1)
    assert 1 not in db._prefix_cache


async def test_all_prefixes():
    await db.set_prefix(1, "?")
    await db.set_prefix(2, "$")
    assert await db.all_prefixes() == {1: "?", 2: "$"}
