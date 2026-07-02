# -*- coding: utf-8 -*-
"""
Install the isolated operator parking_time TEST feature.

This installer only copies Python source files. It does not open or modify
SQLite. The dedicated sandbox migration is a separate next step.
"""

from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "parking_time_test_payload"


def install_one(source: Path, target: Path, backup_root: Path, *, required: bool) -> Path | None:
    if not source.is_file():
        raise FileNotFoundError(f"Payload is missing:\n{source}")
    if required and not target.is_file():
        raise FileNotFoundError(f"Expected project source missing:\n{target}")

    backup = None
    if target.exists():
        backup = backup_root / target.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    py_compile.compile(str(target), doraise=True)
    return backup


def assert_expected(path: Path, markers: tuple[str, ...]) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Expected current source missing:\n{path}")
    source = path.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in source]
    if missing:
        raise RuntimeError(
            "Current source has an unexpected structure; replacement refused:\n"
            f"{path}\nMissing: " + ", ".join(missing)
        )


def main() -> int:
    launcher = ROOT / "run_bot_live_services_sandbox_v1.py"
    profile_handler = ROOT / "Bots" / "handlers" / "profile_verification_workspace.py"

    assert_expected(
        launcher,
        (
            "def integrate_profile_verification(",
            "handle_profile_verification_text",
            "# Прямая кнопка перевірки даних",
        ),
    )
    assert_expected(
        profile_handler,
        (
            "async def show_profile_verification(",
            "resident_confirmation_required",
        ),
    )

    files = [
        (
            PAYLOAD / "profile_parking_time_test_core.py",
            ROOT / "profile_parking_time_test_core.py",
            False,
        ),
        (
            PAYLOAD / "Bots" / "handlers" / "profile_parking_time_test_workspace.py",
            ROOT / "Bots" / "handlers" / "profile_parking_time_test_workspace.py",
            False,
        ),
        (
            PAYLOAD / "run_bot_live_services_sandbox_v1.py",
            launcher,
            True,
        ),
    ]

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_root = (
        ROOT / "Data" / "backups" / "source_code"
        / f"parking_time_test_v1_{stamp}"
    )
    backup_root.mkdir(parents=True, exist_ok=False)

    done: list[tuple[Path, Path | None]] = []
    try:
        for source, target, required in files:
            backup = install_one(source, target, backup_root, required=required)
            done.append((target, backup))
    except Exception:
        for target, backup in reversed(done):
            if backup and backup.is_file():
                shutil.copy2(backup, target)
            elif target.exists():
                target.unlink()
        raise

    print("PARKING_TIME TEST V1 INSTALLATION COMPLETED")
    print("Installed:")
    for _, target, _ in files:
        print(" -", target)
    print("Backups:", backup_root)
    print("Database was not changed.")
    print("Next: RUN_MIGRATE_profile_parking_time_test_sandbox.bat")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("PARKING_TIME TEST V1 INSTALLATION FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
