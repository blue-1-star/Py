# -*- coding: utf-8 -*-
"""
Repair early routing for the resident button:
    📋 Перевірити мої дані

Only the live-services sandbox launcher is replaced. It still patches
Bots/parking_bot.py in memory; Bots/parking_bot.py and the SQLite database
are never written by this installer.
"""

from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOAD = (
    ROOT / "profile_button_early_route_payload"
    / "run_bot_live_services_sandbox_v1.py"
)
TARGET = ROOT / "run_bot_live_services_sandbox_v1.py"


def main() -> int:
    if not PAYLOAD.is_file():
        raise FileNotFoundError(f"Repair payload is missing:\n{PAYLOAD}")
    if not TARGET.is_file():
        raise FileNotFoundError(f"Expected launcher is missing:\n{TARGET}")

    current = TARGET.read_text(encoding="utf-8")
    markers = (
        "def integrate_profile_verification(",
        "handle_profile_verification_text",
        "maybe_show_profile_welcome",
        "def ensure_cashier_route_precedes_client_portal(",
    )
    missing = [marker for marker in markers if marker not in current]
    if missing:
        raise RuntimeError(
            "Current launcher does not match the expected profile-enabled "
            "live-services launcher. Replacement refused. Missing: "
            + ", ".join(missing)
        )

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = (
        ROOT / "Data" / "backups" / "source_code"
        / f"profile_button_early_route_{stamp}"
    )
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup = backup_dir / TARGET.name
    shutil.copy2(TARGET, backup)

    try:
        shutil.copy2(PAYLOAD, TARGET)
        py_compile.compile(str(TARGET), doraise=True)
    except Exception:
        shutil.copy2(backup, TARGET)
        raise

    print("PROFILE BUTTON EARLY-ROUTE FIX COMPLETED")
    print("Replaced:", TARGET)
    print("Backup:", backup)
    print("No database data were changed.")
    print("Next: RUN_CHECK_profile_button_early_route_fix.bat")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("PROFILE BUTTON EARLY-ROUTE FIX FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
