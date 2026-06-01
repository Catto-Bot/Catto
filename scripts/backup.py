"""Online backup of catto.db using SQLite's backup API.

Usage:
    uv run python scripts/backup.py [destination_dir]

Defaults to ./backups/. Creates catto-YYYYmmdd-HHMMSS.db. Safe to run while the bot
is live. SQLite's online backup API holds a shared lock and copies pages
between concurrent writes.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    src = Path("catto.db")
    if not src.exists():
        print(f"source missing: {src}", file=sys.stderr)
        return 1
    dest_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "backups")
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = dest_dir / f"catto-{stamp}.db"
    with sqlite3.connect(src) as source, sqlite3.connect(dest) as backup:
        source.backup(backup)
    print(f"backed up → {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
