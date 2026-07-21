# -*- coding: utf-8 -*-
"""
Reliable installer for the OSBB phone-access UI fix.

It replaces only:
    Bots\handlers\service_orders_workspace.py

Design:
- copies the new file to a temporary file beside the target;
- syntax-checks that temporary file before replacement;
- creates a timestamped backup of the old target;
- clears a possible read-only attribute;
- atomically replaces the target with os.replace().

Usage:
    INSTALL_PHONE_ACCESS_UI_FIX_v2.py
or:
    INSTALL_PHONE_ACCESS_UI_FIX_v2.py --root G:\Programming\Py\OSBB
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


DEFAULT_ROOT = Path(r"G:\Programming\Py\OSBB")
RELATIVE_TARGET = Path("Bots") / "handlers" / "service_orders_workspace.py"


def make_writable(path: Path) -> None:
    """Clear the Windows read-only attribute when possible."""
    if not path.exists():
        return
    try:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IWRITE)
    except OSError:
        # os.replace may still succeed; report a precise error only if it fails.
        pass


def syntax_check(python_exe: Path, file_path: Path) -> None:
    result = subprocess.run(
        [str(python_exe), "-m", "py_compile", str(file_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Python syntax check failed:\n"
            + (result.stdout or "")
            + (result.stderr or "")
        )


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--python", dest="python_exe", default=sys.executable)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    python_exe = Path(args.python_exe).expanduser().resolve()
    package_dir = Path(__file__).resolve().parent
    source = package_dir / RELATIVE_TARGET
    target = root / RELATIVE_TARGET

    print("OSBB phone-access UI fix — reliable installer")
    print()
    print("Source:", source)
    print("Target:", target)

    if not source.is_file():
        raise FileNotFoundError(f"Replacement file is missing:\n{source}")
    if not target.is_file():
        raise FileNotFoundError(
            "Current workspace file was not found:\n"
            f"{target}"
        )
    if not python_exe.is_file():
        raise FileNotFoundError(
            "Python interpreter was not found:\n"
            f"{python_exe}"
        )

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = target.with_name(
        target.name + f".before_phone_access_ui_fix_{stamp}"
    )
    incoming = target.with_name(
        target.name + f".incoming_phone_access_ui_fix_{stamp}"
    )

    # Build a verified replacement before touching the existing file.
    shutil.copy2(source, incoming)
    try:
        syntax_check(python_exe, incoming)
        shutil.copy2(target, backup)
        print("Backup:", backup)

        make_writable(target)
        os.replace(incoming, target)
        syntax_check(python_exe, target)
    except PermissionError as exc:
        incoming.unlink(missing_ok=True)
        raise PermissionError(
            "Windows refused to replace the target file.\n\n"
            "1. Stop Start_OSBB_Live_Services_Sandbox_Bot_v1.bat with Ctrl+C.\n"
            "2. Close the target file in VS Code / Notepad++ if it is open.\n"
            "3. Run this installer again.\n\n"
            f"Target: {target}\n"
            f"Windows message: {exc}"
        ) from exc
    except Exception:
        incoming.unlink(missing_ok=True)
        raise

    print()
    print("SUCCESS")
    print("Installed:", target)
    print("Backup:", backup)
    print("Start the live-services sandbox bot again.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print()
        print("INSTALL FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
