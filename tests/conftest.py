import pytest

from core import db


@pytest.fixture(autouse=True)
async def fresh_db(tmp_path, monkeypatch):
    """Reset the module-level connection to a fresh tmp DB per test."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    monkeypatch.setattr(db, "_conn", None)
    monkeypatch.setattr(db, "_prefix_cache", {})
    await db.init_db()
    yield
    await db.close_db()
