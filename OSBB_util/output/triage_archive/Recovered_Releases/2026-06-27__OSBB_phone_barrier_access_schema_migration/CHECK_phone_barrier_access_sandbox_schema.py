# -*- coding: utf-8 -*-
"""Read-only verification of the phone-barrier access sandbox schema."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SANDBOX_DB = (
    ROOT
    / "Data"
    / "db"
    / "sandbox"
    / "osbb_test_live_services_2026-06-26_20-13-26.db"
)


def main() -> int:
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)

    from phone_barrier_access_core import (
        ACCESS_POLICY_SET,
        TARIFF_CONNECT,
        TARIFF_MONTHLY,
        required_phone_access_tables,
        table_exists,
    )

    if not SANDBOX_DB.is_file():
        raise FileNotFoundError(f"Sandbox database not found:\n{SANDBOX_DB}")

    conn = sqlite3.connect(SANDBOX_DB)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        missing = sorted(
            table for table in required_phone_access_tables()
            if not table_exists(cur, table)
        )
        if missing:
            print("SCHEMA NOT READY")
            print("Missing:", ", ".join(missing))
            return 2

        print("OSBB phone-barrier access sandbox schema")
        print("Database:", SANDBOX_DB)
        print("Result: all required tables present")
        print()

        print("Access points:")
        for row in cur.execute(
            """
            SELECT access_point_code, display_name_uk, point_status, is_active
            FROM access_points
            ORDER BY access_point_code
            """
        ):
            print(
                f" - {row['access_point_code']}: {row['display_name_uk']} "
                f"| {row['point_status']} | active={row['is_active']}"
            )

        print()
        print("Active tariffs:")
        for row in cur.execute(
            """
            SELECT tariff_code, amount, currency, billing_period, effective_from
            FROM access_tariff_versions
            WHERE tariff_code IN (?, ?)
              AND version_status = 'ACTIVE'
            ORDER BY tariff_code, effective_from
            """,
            (TARIFF_CONNECT, TARIFF_MONTHLY),
        ):
            print(
                f" - {row['tariff_code']}: {row['amount']} {row['currency']} "
                f"| {row['billing_period']} | from {row['effective_from']}"
            )

        print()
        print("Active policy:")
        policy = cur.execute(
            """
            SELECT id, version_number, effective_from
            FROM access_policy_versions
            WHERE policy_set_code = ? AND policy_status = 'ACTIVE'
            ORDER BY effective_from DESC, version_number DESC
            LIMIT 1
            """,
            (ACCESS_POLICY_SET,),
        ).fetchone()
        if not policy:
            raise RuntimeError("No active phone-barrier policy found.")
        print(
            f" - {ACCESS_POLICY_SET} v{policy['version_number']} "
            f"| from {policy['effective_from']}"
        )
        for row in cur.execute(
            """
            SELECT setting_code, value_text
            FROM access_policy_values
            WHERE policy_version_id = ?
            ORDER BY setting_code
            """,
            (int(policy["id"]),),
        ):
            print(f"   {row['setting_code']} = {row['value_text']}")

        print()
        print("Existing subscriptions:", cur.execute(
            "SELECT COUNT(*) FROM phone_access_subscriptions"
        ).fetchone()[0])
        print("Existing warnings:", cur.execute(
            "SELECT COUNT(*) FROM access_debt_warnings"
        ).fetchone()[0])
        print("CHECK COMPLETED")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
