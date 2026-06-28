# -*- coding: utf-8 -*-
"""
Apply terminology/readiness correction for resident profile verification.

This patch changes only Python sources:
- profile_verification_core.py
- Bots/handlers/profile_verification_workspace.py
- Bots/handlers/service_orders_workspace.py

It does NOT change SQLite data, vehicles, contacts, payments, orders,
subscriptions, or access rights.
"""

from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "profile_verification_terminology_v2_payload"


def install_one(source: Path, target: Path, backup_root: Path) -> Path | None:
    if not source.is_file():
        raise FileNotFoundError(f"Payload file is missing:\n{source}")
    existed = target.exists()
    backup: Path | None = None
    if existed:
        backup = backup_root / target.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    py_compile.compile(str(target), doraise=True)
    return backup


def require_marker(path: Path, markers: tuple[str, ...]) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Expected project source missing:\n{path}")
    source = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise RuntimeError(
            "Current source has an unexpected structure; automatic replacement "
            f"refused:\n{path}\nMissing: " + ", ".join(missing)
        )


def main() -> int:
    targets = [
        (
            PAYLOAD / "profile_verification_core.py",
            ROOT / "profile_verification_core.py",
            (
                "def profile_snapshot(",
                "def confirm_profile(",
                "PROFILE_ALLOW_PRIVATE_ACCESS_PHONE",
            ),
        ),
        (
            PAYLOAD / "Bots" / "handlers" / "profile_verification_workspace.py",
            ROOT / "Bots" / "handlers" / "profile_verification_workspace.py",
            (
                "async def show_profile_verification(",
                "PARKING_BUTTONS",
                "BUTTON_CONFIRM",
            ),
        ),
        (
            PAYLOAD / "Bots" / "handlers" / "service_orders_workspace.py",
            ROOT / "Bots" / "handlers" / "service_orders_workspace.py",
            (
                "def _phone_profile_gate_text(",
                "phone_access_eligibility",
            ),
        ),
    ]

    for _, target, markers in targets:
        require_marker(target, markers)

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_root = (
        ROOT / "Data" / "backups" / "source_code"
        / f"profile_verification_terminology_v2_{stamp}"
    )
    backup_root.mkdir(parents=True, exist_ok=False)

    completed: list[tuple[Path, Path | None]] = []
    try:
        for source, target, _ in targets:
            backup = install_one(source, target, backup_root)
            completed.append((target, backup))
    except Exception:
        for target, backup in reversed(completed):
            if backup and backup.is_file():
                shutil.copy2(backup, target)
            elif target.exists():
                target.unlink()
        raise

    print("PROFILE VERIFICATION TERMINOLOGY V2 COMPLETED")
    print("Replaced:")
    for _, target, _ in targets:
        print(" -", target)
    print("Backups:", backup_root)
    print()
    print("No database data were changed.")
    print("Restart Start_OSBB_Live_Services_Sandbox_Bot_v1.bat after this.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("PROFILE VERIFICATION TERMINOLOGY V2 FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
