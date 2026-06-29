# -*- coding: utf-8 -*-
"""
Create TEST-only parking_time session tables in the live-services sandbox.

No resident, vehicle, payment, order or access tables are modified.
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SANDBOX_DB = (
    ROOT / "Data" / "db" / "sandbox"
    / "osbb_test_live_services_2026-06-26_20-13-26.db"
)
BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
LOG_DIR = ROOT / "Data" / "db" / "logs"


def main() -> int:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from profile_parking_time_test_core import ensure_test_schema

    print("OSBB isolated parking_time TEST migration")
    print("Mode: SANDBOX ONLY")
    print("Purpose: dedicated TEST tables; source vehicles remain untouched")
    print("Database:", SANDBOX_DB)

    if not SANDBOX_DB.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")

    conn = sqlite3.connect(SANDBOX_DB)
    try:
        tables = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        missing = {"apartments", "vehicles"} - tables
        if missing:
            raise RuntimeError(
                "This is not the expected live-services sandbox. Missing: "
                + ", ".join(sorted(missing))
            )
    finally:
        conn.close()

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BACKUP_DIR / (
        f"{SANDBOX_DB.stem}_before_profile_parking_time_test_{stamp}{SANDBOX_DB.suffix}"
    )
    shutil.copy2(SANDBOX_DB, backup)
    print("Backup:", backup)

    conn = sqlite3.connect(SANDBOX_DB)
    try:
        conn.execute("BEGIN IMMEDIATE")
        changes = ensure_test_schema(
            conn,
            actor_id="sandbox_parking_time_test_migration",
            sandbox_db_path=str(SANDBOX_DB),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = LOG_DIR / f"profile_parking_time_test_migration_{stamp}.txt"
    log.write_text(
        "\n".join(
            [
                "OSBB isolated parking_time TEST migration",
                "Mode: SANDBOX ONLY",
                f"Database: {SANDBOX_DB}",
                f"Backup: {backup}",
                "Changes:",
                *[f"- {line}" for line in changes],
                "MIGRATION COMPLETED",
            ]
        ) + "\n",
        encoding="utf-8",
    )
    print("Changes:")
    for line in changes:
        print(" -", line)
    print("Log:", log)
    print("MIGRATION COMPLETED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("MIGRATION FAILED:", type(exc).__name__ + ":", exc)
        traceback.print_exc()
        raise SystemExit(1)
