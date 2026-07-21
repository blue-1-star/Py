# -*- coding: utf-8 -*-
"""
Apply the phone-barrier access schema ONLY to the designated live-services
sandbox database.

It creates an SQLite backup before any database write and refuses every other
database path. It does not start the bot or touch osbb.db.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
import traceback
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SANDBOX_DB = (
    ROOT
    / "Data"
    / "db"
    / "sandbox"
    / "osbb_test_live_services_2026-06-26_20-13-26.db"
)
BACKUP_DIR = ROOT / "Data" / "db" / "sandbox" / "backups"
LOG_DIR = ROOT / "Data" / "db" / "logs"


def import_core():
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    from phone_barrier_access_core import (
        ensure_phone_barrier_access_schema,
        required_phone_access_tables,
        table_exists,
    )
    return ensure_phone_barrier_access_schema, required_phone_access_tables, table_exists


def write_log(stamp: str, lines: list[str]) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = LOG_DIR / f"phone_barrier_access_schema_migration_{stamp}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OSBB phone-barrier access schema migration (sandbox only)."
    )
    parser.add_argument(
        "--effective-from",
        default=date.today().isoformat(),
        help="Initial sandbox tariff/policy date, YYYY-MM-DD.",
    )
    args = parser.parse_args()

    effective_from = date.fromisoformat(args.effective_from).isoformat()
    ensure_schema, required_tables, table_exists = import_core()

    print("OSBB phone-barrier access schema migration")
    print("Mode: SANDBOX ONLY")
    print("Database:", SANDBOX_DB)
    print("Effective from:", effective_from)

    if not SANDBOX_DB.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")

    expected_parent = (ROOT / "Data" / "db" / "sandbox").resolve()
    if SANDBOX_DB.resolve().parent != expected_parent:
        raise RuntimeError("Safety check failed: database is not inside the sandbox directory.")

    conn = sqlite3.connect(SANDBOX_DB)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        required_existing = {"service_orders", "payments", "service_order_interests"}
        missing_existing = sorted(
            name for name in required_existing if not table_exists(cur, name)
        )
        if missing_existing:
            raise RuntimeError(
                "This is not the expected live-services sandbox. "
                "Missing existing tables: " + ", ".join(missing_existing)
            )
        print("Preflight:")
        print("  existing service tables: present")
        print("  new phone-access tables before migration:",
              sum(1 for name in required_tables() if table_exists(cur, name)),
              "of", len(required_tables()))
    finally:
        conn.close()

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / (
        f"{SANDBOX_DB.stem}_before_phone_barrier_access_schema_{stamp}{SANDBOX_DB.suffix}"
    )
    shutil.copy2(SANDBOX_DB, backup)
    print("Backup:", backup)

    conn = sqlite3.connect(SANDBOX_DB)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN IMMEDIATE")
        changes = ensure_schema(
            conn,
            effective_from=effective_from,
            actor_id="sandbox_phone_barrier_access_migration",
            sandbox_db_path=str(SANDBOX_DB),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    log_lines = [
        "OSBB phone-barrier access schema migration",
        "Mode: SANDBOX ONLY",
        f"Database: {SANDBOX_DB}",
        f"Effective from: {effective_from}",
        f"Backup: {backup}",
        "Changes:",
        *[f"- {item}" for item in changes],
        "Result: MIGRATION COMPLETED",
    ]
    log = write_log(stamp, log_lines)

    print("Changes:")
    for item in changes:
        print(" -", item)
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
