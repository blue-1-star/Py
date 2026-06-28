# -*- coding: utf-8 -*-
"""
Hide the resident profile confirmation button after the profile becomes READY.

Only this file is replaced:
    Bots/handlers/profile_verification_workspace.py

No SQLite data, vehicles, contacts, payments, orders or subscriptions are changed.
"""

from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOAD = (
    ROOT / "profile_confirmation_button_ready_payload"
    / "Bots" / "handlers" / "profile_verification_workspace.py"
)
TARGET = ROOT / "Bots" / "handlers" / "profile_verification_workspace.py"


def main() -> int:
    if not PAYLOAD.is_file():
        raise FileNotFoundError(f"Repair payload missing:\n{PAYLOAD}")
    if not TARGET.is_file():
        raise FileNotFoundError(f"Expected handler missing:\n{TARGET}")

    current = TARGET.read_text(encoding="utf-8")
    markers = (
        "async def show_profile_verification(",
        "critical_codes = {",
        "structural_codes = {",
        "resident_confirmation_required",
    )
    missing = [marker for marker in markers if marker not in current]
    if missing:
        raise RuntimeError(
            "Installed handler does not match the expected profile-verification "
            "version. Replacement refused. Missing: " + ", ".join(missing)
        )

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = (
        ROOT / "Data" / "backups" / "source_code"
        / f"profile_confirmation_ready_visibility_{stamp}"
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

    print("PROFILE CONFIRMATION READY-VISIBILITY FIX COMPLETED")
    print("Replaced:", TARGET)
    print("Backup:", backup)
    print("No SQLite data were changed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("PROFILE CONFIRMATION READY-VISIBILITY FIX FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
