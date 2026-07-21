# -*- coding: utf-8 -*-
r"""
Apply the simplified paid-preorder workflow only to the dedicated live-services
sandbox database. It does not touch osbb.db or other sandbox files.

The migration is additive: it preserves historical service_orders and adds
interest / supplier-batch tables plus the new REMOTE_NEW_PREORDER profile.
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SANDBOX = ROOT / "Data" / "db" / "sandbox" / "osbb_test_live_services_2026-06-26_20-13-26.db"
BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
LOGS = ROOT / "Data" / "db" / "logs"


def main() -> int:
    print("OSBB simplified paid-preorder workflow migration")
    print("Sandbox:", SANDBOX)
    if not SANDBOX.is_file():
        raise FileNotFoundError("Live-services sandbox DB was not found.")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BACKUPS / f"{SANDBOX.stem}_before_simplified_services_{stamp}{SANDBOX.suffix}"
    shutil.copy2(SANDBOX, backup)
    print("Backup:", backup)

    # Import after the source files have been copied to the project root.
    from service_preorders_core import ensure_simplified_service_schema

    conn = sqlite3.connect(SANDBOX)
    try:
        changes = ensure_simplified_service_schema(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    LOGS.mkdir(parents=True, exist_ok=True)
    log = LOGS / f"simplified_services_migration_{stamp}.txt"
    log.write_text(
        "Simplified services sandbox migration\n"
        f"Sandbox: {SANDBOX}\n"
        f"Backup: {backup}\n"
        + "\n".join(changes or ["Schema already up to date."])
        + "\n",
        encoding="utf-8",
    )
    print("Changes:")
    for line in changes or ["Schema already up to date."]:
        print(" -", line)
    print("Log:", log)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("MIGRATION FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
