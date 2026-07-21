# -*- coding: utf-8 -*-
"""
Restore the live-services sandbox launcher that routes cashier v2 before the
client portal fallback.

This installer changes only:
    run_bot_live_services_sandbox_v1.py

It does not change:
- SQLite databases;
- Bots/parking_bot.py;
- service-order workspace;
- phone-access tables;
- payment notifications.

A timestamped source backup is created first.
"""

from __future__ import annotations

import argparse
import py_compile
import shutil
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PAYLOAD = (
    SCRIPT_DIR
    / "cashier_route_repair_payload"
    / "run_bot_live_services_sandbox_v1.py"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=str(SCRIPT_DIR),
        help="OSBB root (default: folder containing this installer).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    target = root / "run_bot_live_services_sandbox_v1.py"
    bot = root / "Bots" / "parking_bot.py"
    switcher = root / "switch_parking_bot_to_cashier_v2.py"
    patcher = root / "patch_parking_bot_service_orders_v1.py"

    if not PAYLOAD.is_file():
        raise FileNotFoundError(f"Repair payload is missing:\n{PAYLOAD}")
    for required in (target, bot, switcher, patcher):
        if not required.is_file():
            raise FileNotFoundError(
                "This is not the expected OSBB project root. Missing:\n"
                f"{required}"
            )

    current = target.read_text(encoding="utf-8")
    if "def patch_bot_source()" not in current:
        raise RuntimeError(
            "Current launcher does not match the expected live-services launcher; "
            "it will not be overwritten automatically."
        )

    incoming = PAYLOAD.read_text(encoding="utf-8")
    if "def ensure_cashier_route_precedes_client_portal(" not in incoming:
        raise RuntimeError("Repair payload is incomplete.")

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = root / "Data" / "backups" / "source_code" / f"cashier_route_repair_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup = backup_dir / target.name
    shutil.copy2(target, backup)

    try:
        shutil.copy2(PAYLOAD, target)
        py_compile.compile(str(target), doraise=True)
    except Exception:
        shutil.copy2(backup, target)
        raise

    print("CASHIER ROUTE REPAIR COMPLETED")
    print("OSBB root:", root)
    print("Replaced:", target)
    print("Backup:", backup)
    print()
    print("Next run:")
    print("  RUN_CHECK_cashier_route_after_phone_v2.bat")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("CASHIER ROUTE REPAIR FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
