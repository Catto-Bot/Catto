from core import db


async def test_first_claim_returns_true():
    is_new = await db.record_anicat_claim(1, "alice", "Jett", 100)
    assert is_new is True


async def test_duplicate_claim_returns_false():
    await db.record_anicat_claim(1, "alice", "Jett", 100)
    is_new = await db.record_anicat_claim(1, "alice", "Jett", 100)
    assert is_new is False


async def test_claim_bumps_totals():
    await db.record_anicat_claim(1, "alice", "Jett", 100)
    await db.record_anicat_claim(1, "alice", "Raze", 50)
    user = await db.get_anicat_user(1)
    assert user["total_cats"] == 2
    assert user["total_pts"] == 150


async def test_list_claims_alphabetical():
    await db.record_anicat_claim(1, "alice", "Raze", 50)
    await db.record_anicat_claim(1, "alice", "Jett", 100)
    assert await db.list_anicat_claims(1) == ["Jett", "Raze"]
