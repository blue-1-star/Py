# -*- coding: utf-8 -*-
"""
Read-only verification for the isolated parking_time TEST feature.

It does not open a TEST session and does not write to any table.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SANDBOX_DB = (
    ROOT / "Data" / "db" / "sandbox"
    / "osbb_test_live_services_2026-06-26_20-13-26.db"
)


def main() -> int:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from profile_parking_time_test_core import (
        TEST_SCHEMA_MIGRATION_CODE,
        TEST_TARGET_APARTMENT,
        required_test_tables,
        table_exists,
        test_candidate,
    )

    print("OSBB isolated parking_time TEST check")
    print("Read-only check.")
    print("Database:", SANDBOX_DB)

    if not SANDBOX_DB.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")

    uri = SANDBOX_DB.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA query_only = ON")
        cur = conn.cursor()
        missing = sorted(
            name for name in required_test_tables()
            if not table_exists(cur, name)
        )
        if missing:
            raise RuntimeError("Missing TEST tables: " + ", ".join(missing))

        marker = cur.execute(
            """
            SELECT migration_code
            FROM profile_parking_time_test_schema_migrations
            WHERE migration_code = ?
            """,
            (TEST_SCHEMA_MIGRATION_CODE,),
        ).fetchone()
        if not marker:
            raise RuntimeError("TEST migration marker is absent.")

        candidate = test_candidate(
            apartment_number=TEST_TARGET_APARTMENT,
            conn=conn,
        )
        print("Result: TEST schema and marker present")
        print()
        print(
            f"Candidate apartment: {candidate.get('apartment_number')} "
            f"| id={candidate.get('apartment_id')}"
        )
        if candidate.get("vehicles"):
            for row in candidate["vehicles"]:
                print(
                    f" - vehicle id={row.get('id')} | {row.get('plate') or 'без номера'} "
                    f"| parking_time=EMPTY"
                )
        else:
            print(" - no vehicle with empty parking_time (TEST UI will refuse to open).")

        count = cur.execute(
            "SELECT COUNT(*) FROM profile_parking_time_test_sessions"
        ).fetchone()[0]
        print()
        print("Existing TEST sessions:", count)
        print("CHECK COMPLETED")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
