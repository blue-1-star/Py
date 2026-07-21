# -*- coding: utf-8 -*-
"""
Restore compatibility with sandbox databases that use base_service_code.

This repair replaces only three Python source files. It does not write to any
SQLite database, create payment notices, confirm payments, or start the bot.
"""

from __future__ import annotations

import argparse
import py_compile
import shutil
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PAYLOAD = SCRIPT_DIR / "service_code_compatibility_payload"


def copy_checked(source: Path, target: Path, backup_dir: Path) -> Path:
    if not source.is_file():
        raise FileNotFoundError(f"Repair payload missing:\n{source}")
    if not target.is_file():
        raise FileNotFoundError(f"Expected project source missing:\n{target}")
    backup = backup_dir / target.relative_to(ROOT)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target, backup)
    shutil.copy2(source, target)
    py_compile.compile(str(target), doraise=True)
    return backup


def main() -> int:
    global ROOT

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=str(SCRIPT_DIR),
        help="OSBB root (default: folder containing this installer).",
    )
    args = parser.parse_args()
    ROOT = Path(args.root).resolve()

    targets = {
        PAYLOAD / "service_orders_core.py": ROOT / "service_orders_core.py",
        PAYLOAD / "service_preorders_core.py": ROOT / "service_preorders_core.py",
        PAYLOAD / "Bots" / "handlers" / "service_orders_workspace.py":
            ROOT / "Bots" / "handlers" / "service_orders_workspace.py",
    }

    # Guard against copying into a wrong unrelated folder.
    expected_markers = {
        ROOT / "service_orders_core.py": "def link_payment_to_order(",
        ROOT / "service_preorders_core.py": "def reconcile_paid_service_interests(",
        ROOT / "Bots" / "handlers" / "service_orders_workspace.py": "def _current_offers()",
    }
    for target, marker in expected_markers.items():
        if not target.is_file():
            raise FileNotFoundError(f"Expected OSBB source missing:\n{target}")
        if marker not in target.read_text(encoding="utf-8"):
            raise RuntimeError(
                "Current source does not have the expected structure; "
                f"automatic replacement refused:\n{target}"
            )

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = ROOT / "Data" / "backups" / "source_code" / f"service_code_compatibility_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    done: list[tuple[Path, Path]] = []
    try:
        for source, target in targets.items():
            backup = copy_checked(source, target, backup_dir)
            done.append((target, backup))
    except Exception:
        for target, backup in reversed(done):
            shutil.copy2(backup, target)
        raise

    print("SERVICE-CODE COMPATIBILITY REPAIR COMPLETED")
    print("OSBB root:", ROOT)
    print("Backups:", backup_dir)
    print("Replaced:")
    for _, target in targets.items():
        print(" -", target)
    print()
    print("This repair did not change the sandbox database.")
    print("Next: RUN_CHECK_service_code_compatibility_phone_v2.bat")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("SERVICE-CODE COMPATIBILITY REPAIR FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
