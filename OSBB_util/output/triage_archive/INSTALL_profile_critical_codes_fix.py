# -*- coding: utf-8 -*-
"""
Fix the undefined critical_codes variable in resident profile verification.

Only the profile UI handler is replaced:
    Bots/handlers/profile_verification_workspace.py

No database data are changed.
"""

from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOAD = (
    ROOT / "profile_verification_critical_codes_payload"
    / "Bots" / "handlers" / "profile_verification_workspace.py"
)
TARGET = ROOT / "Bots" / "handlers" / "profile_verification_workspace.py"


def main() -> int:
    if not PAYLOAD.is_file():
        raise FileNotFoundError(f"Missing repair payload:\n{PAYLOAD}")
    if not TARGET.is_file():
        raise FileNotFoundError(f"Expected handler missing:\n{TARGET}")

    current = TARGET.read_text(encoding="utf-8")
    markers = (
        "async def show_profile_verification(",
        "structural_codes = {",
        'if "CONFIRM_NO_VEHICLE" in critical_codes:',
        'if "PARKING_TIME" in critical_codes:',
    )
    missing = [marker for marker in markers if marker not in current]
    if missing:
        raise RuntimeError(
            "Current handler does not match the expected terminology V2 "
            "version. Replacement refused. Missing: " + ", ".join(missing)
        )

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = (
        ROOT / "Data" / "backups" / "source_code"
        / f"profile_critical_codes_fix_{stamp}"
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

    print("PROFILE CRITICAL-CODES FIX COMPLETED")
    print("Replaced:", TARGET)
    print("Backup:", backup)
    print("No SQLite data were changed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("PROFILE CRITICAL-CODES FIX FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
