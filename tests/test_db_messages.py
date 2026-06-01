from core import db


async def test_first_message_count_is_one():
    total = await db.bump_message_count(1, "alice")
    assert total == 1


async def test_each_bump_increments():
    await db.bump_message_count(1, "alice")
    await db.bump_message_count(1, "alice")
    total = await db.bump_message_count(1, "alice")
    assert total == 3


async def test_username_updates_on_each_bump():
    await db.bump_message_count(1, "old_name")
    total = await db.bump_message_count(1, "new_name")
    assert total == 2
