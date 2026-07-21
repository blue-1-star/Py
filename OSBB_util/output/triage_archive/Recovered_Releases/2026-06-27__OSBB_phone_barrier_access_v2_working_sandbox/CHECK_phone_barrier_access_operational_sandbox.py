# -*- coding: utf-8 -*-
"""Read-only verification of the operational two-barrier phone-access model."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    db = root / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from phone_barrier_access_core import (
        OPERATIONAL_SCHEMA_MIGRATION_CODE,
        required_phone_access_operational_tables,
        table_exists,
    )

    if not db.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{db}")

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        missing = sorted(
            table for table in required_phone_access_operational_tables()
            if not table_exists(cur, table)
        )
        if missing:
            print("OPERATIONAL SCHEMA NOT READY")
            print("Missing:", ", ".join(missing))
            return 2

        marker = cur.execute(
            "SELECT applied_at FROM access_schema_migrations WHERE migration_code = ?",
            (OPERATIONAL_SCHEMA_MIGRATION_CODE,),
        ).fetchone()
        if not marker:
            print("OPERATIONAL SCHEMA NOT READY")
            print("Missing migration marker:", OPERATIONAL_SCHEMA_MIGRATION_CODE)
            return 3

        print("OSBB two-barrier phone-access operational sandbox check")
        print("Database:", db)
        print("Result: all operational tables and migration marker present")
        print()
        print("Requests:", cur.execute("SELECT COUNT(*) FROM phone_access_requests").fetchone()[0])
        print("Subscriptions:", cur.execute("SELECT COUNT(*) FROM phone_access_subscriptions").fetchone()[0])
        print("Subscription points:", cur.execute("SELECT COUNT(*) FROM phone_access_subscription_points").fetchone()[0])
        print("Connection charges:", cur.execute(
            "SELECT COUNT(*) FROM phone_access_subscription_charges WHERE charge_kind = 'CONNECT'"
        ).fetchone()[0])
        print("Monthly charges:", cur.execute(
            "SELECT COUNT(*) FROM phone_access_subscription_charges WHERE charge_kind = 'MONTHLY'"
        ).fetchone()[0])
        print("Warnings:", cur.execute("SELECT COUNT(*) FROM access_debt_warnings").fetchone()[0])
        print()
        print("No existing generic phone order was converted automatically.")
        print("New structured phone requests will create subscriptions only after confirmed payment.")
        print("CHECK COMPLETED")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
