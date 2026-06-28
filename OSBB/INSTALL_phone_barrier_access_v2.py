# -*- coding: utf-8 -*-
"""
Install the code layer for the two-barrier phone-access model.

This script changes Python sources only. It does not start the bot and does not
write any SQLite database. Run the separate operational migration afterwards.
"""

from __future__ import annotations

import argparse
import py_compile
import shutil
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PAYLOAD_DIR = SCRIPT_DIR / "phone_barrier_access_v2_payload"


REQUIRED_MARKERS = {
    "phone_barrier_access_core.py": [
        "SCHEMA_MIGRATION_CODE = \"PHONE_BARRIER_ACCESS_SCHEMA_V1\"",
        "def ensure_phone_barrier_access_schema(",
    ],
    "service_orders_core.py": [
        "def create_service_order(",
        "def activate_access_credential(",
    ],
    "service_preorders_core.py": [
        "def create_service_interest(",
        "def reconcile_paid_service_interests(",
    ],
    "Bots/handlers/service_orders_workspace.py": [
        "def _requested_phone(",
        "def _is_phone_offer(",
        "async def handle_service_orders_text(",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=str(SCRIPT_DIR),
        help="OSBB root. Default: folder containing this installer.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not PAYLOAD_DIR.is_dir():
        raise FileNotFoundError(f"Payload folder is missing:\n{PAYLOAD_DIR}")

    target_relatives = [
        Path("phone_barrier_access_core.py"),
        Path("phone_barrier_access_service.py"),
        Path("service_orders_core.py"),
        Path("service_preorders_core.py"),
        Path("Bots/handlers/service_orders_workspace.py"),
    ]

    # Validate the known pre-V2 sources before touching any file.
    for relative, markers in REQUIRED_MARKERS.items():
        target = root / relative
        if not target.is_file():
            raise FileNotFoundError(f"Required source is missing:\n{target}")
        source = read_text(target)
        missing = [marker for marker in markers if marker not in source]
        if missing:
            raise RuntimeError(
                "Source does not match the expected tested baseline and will not be replaced:\n"
                f"{target}\nMissing marker: {missing[0]}"
            )

    for relative in target_relatives:
        source = PAYLOAD_DIR / relative
        if not source.is_file():
            raise FileNotFoundError(f"Payload source is missing:\n{source}")

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_root = root / "Data" / "backups" / "source_code" / f"phone_barrier_access_v2_{stamp}"
    backup_root.mkdir(parents=True, exist_ok=False)

    copied: list[tuple[Path, Path]] = []
    try:
        for relative in target_relatives:
            target = root / relative
            source = PAYLOAD_DIR / relative
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                shutil.copy2(target, backup)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append((target, backup))

        for target, _backup in copied:
            py_compile.compile(str(target), doraise=True)

    except Exception:
        # Restore all existing files that were backed up. If phone_barrier_access_service.py
        # did not exist before, remove the just-created copy.
        for target, backup in reversed(copied):
            if backup.exists():
                shutil.copy2(backup, target)
            elif target.exists():
                target.unlink()
        raise

    print("CODE INSTALLATION COMPLETED")
    print("OSBB root:", root)
    print("Source backup:", backup_root)
    print("Updated sources:")
    for target, _backup in copied:
        print(" -", target.relative_to(root))
    print()
    print("No database was changed.")
    print("Next: run RUN_MIGRATE_phone_barrier_access_operational_sandbox.bat")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("INSTALLATION FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
