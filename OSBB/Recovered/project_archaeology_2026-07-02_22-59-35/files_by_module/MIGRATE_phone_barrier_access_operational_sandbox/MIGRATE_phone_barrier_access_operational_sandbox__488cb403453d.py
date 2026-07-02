# -*- coding: utf-8 -*-
"""
Apply the operational two-barrier phone-access tables ONLY to the designated
live-services sandbox.

Prerequisite:
- V1 schema migration completed successfully.
- Code package installed; this script needs the updated phone_barrier_access_core.py.

The script creates a full SQLite backup before the write transaction.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent),
        help="OSBB root. Default: directory of this script.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    db = (
        root
        / "Data"
        / "db"
        / "sandbox"
        / "osbb_test_live_services_2026-06-26_20-13-26.db"
    )
    backups = root / "Data" / "db" / "sandbox" / "backups"
    logs = root / "Data" / "db" / "logs"

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from phone_barrier_access_core import (
        OPERATIONAL_SCHEMA_MIGRATION_CODE,
        SCHEMA_MIGRATION_CODE,
        ensure_phone_access_operational_schema,
        required_phone_access_operational_tables,
        table_exists,
    )

    print("OSBB two-barrier phone-access operational migration")
    print("Mode: SANDBOX ONLY")
    print("Database:", db)

    if not db.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{db}")
    if db.resolve().parent != (root / "Data" / "db" / "sandbox").resolve():
        raise RuntimeError("Safety check failed: target is not the live-services sandbox.")

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        if not table_exists(cur, "access_schema_migrations"):
            raise RuntimeError(
                "V1 schema has not been applied. Run RUN_MIGRATE_phone_barrier_access_sandbox.bat first."
            )
        row = cur.execute(
            "SELECT 1 FROM access_schema_migrations WHERE migration_code = ?",
            (SCHEMA_MIGRATION_CODE,),
        ).fetchone()
        if not row:
            raise RuntimeError("V1 migration marker is missing; operational migration is refused.")
        required_existing = {"service_orders", "service_order_interests", "service_access_credentials"}
        missing_existing = sorted(
            name for name in required_existing if not table_exists(cur, name)
        )
        if missing_existing:
            raise RuntimeError(
                "This is not the expected live-services sandbox. Missing: "
                + ", ".join(missing_existing)
            )
        existing = sum(
            1 for table in required_phone_access_operational_tables()
            if table_exists(cur, table)
        )
    finally:
        conn.close()

    print("Preflight:")
    print("  V1 migration marker: present")
    print("  operational tables before migration:", existing, "of", len(required_phone_access_operational_tables()))

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backups.mkdir(parents=True, exist_ok=True)
    backup = backups / f"{db.stem}_before_phone_barrier_access_operational_{stamp}{db.suffix}"
    shutil.copy2(db, backup)
    print("Backup:", backup)

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN IMMEDIATE")
        changes = ensure_phone_access_operational_schema(
            conn,
            actor_id="sandbox_phone_barrier_access_operational_migration",
            sandbox_db_path=str(db),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    logs.mkdir(parents=True, exist_ok=True)
    log = logs / f"phone_barrier_access_operational_migration_{stamp}.txt"
    lines = [
        "OSBB two-barrier phone-access operational migration",
        "Mode: SANDBOX ONLY",
        f"Database: {db}",
        f"Backup: {backup}",
        "Changes:",
        *[f"- {item}" for item in changes],
        f"Result: {OPERATIONAL_SCHEMA_MIGRATION_CODE} COMPLETED",
    ]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")

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
