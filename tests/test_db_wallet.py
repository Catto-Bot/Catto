from core import db


async def test_wallet_does_not_exist_initially():
    assert not await db.wallet_exists(1)


async def test_create_wallet_starts_at_zero():
    await db.create_wallet(1, "alice")
    w = await db.get_wallet(1)
    assert w["coins"] == 0
    assert w["username"] == "alice"


async def test_update_coins_adds():
    await db.create_wallet(1, "alice")
    await db.update_coins(1, 500)
    assert (await db.get_wallet(1))["coins"] == 500


async def test_transfer_moves_balance():
    await db.create_wallet(1, "alice")
    await db.create_wallet(2, "bob")
    await db.update_coins(1, 1000)
    await db.transfer(1, 2, 400)
    assert (await db.get_wallet(1))["coins"] == 600
    assert (await db.get_wallet(2))["coins"] == 400


async def test_top_wallets_orders_desc():
    for i, (name, coins) in enumerate([("a", 100), ("b", 500), ("c", 200)], 1):
        await db.create_wallet(i, name)
        await db.update_coins(i, coins)
    top = await db.top_wallets(10)
    assert [w["username"] for w in top] == ["b", "c", "a"]


async def test_get_wallet_returns_none_for_missing():
    assert await db.get_wallet(999) is None
