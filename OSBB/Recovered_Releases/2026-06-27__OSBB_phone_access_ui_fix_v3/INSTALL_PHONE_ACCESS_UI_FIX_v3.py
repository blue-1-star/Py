# -*- coding: utf-8 -*-
"""
Reliable installer for OSBB phone-access UI fix v3.
Replaces only Bots\handlers\service_orders_workspace.py.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_ROOT = Path(r"G:\Programming\Py\OSBB")
RELATIVE_TARGET = Path("Bots") / "handlers" / "service_orders_workspace.py"


def make_writable(path: Path) -> None:
    if not path.exists():
        return
    try:
        path.chmod(path.stat().st_mode | stat.S_IWRITE)
    except OSError:
        pass


def syntax_check(python_exe: Path, file_path: Path) -> None:
    result = subprocess.run(
        [str(python_exe), "-m", "py_compile", str(file_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
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

    print("OSBB phone-access UI fix v3")
    print()
    print("Source:", source)
    print("Target:", target)

    if not source.is_file():
        raise FileNotFoundError(f"Replacement file is missing:\n{source}")
    if not target.is_file():
        raise FileNotFoundError(f"Current workspace file was not found:\n{target}")
    if not python_exe.is_file():
        raise FileNotFoundError(f"Python interpreter was not found:\n{python_exe}")

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = target.with_name(target.name + f".before_phone_access_ui_fix_v3_{stamp}")
    incoming = target.with_name(target.name + f".incoming_phone_access_ui_fix_v3_{stamp}")

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
            "2. Close service_orders_workspace.py in VS Code / Notepad++.\n"
            "3. Run this installer again.\n\n"
            f"Target: {target}\nWindows message: {exc}"
        ) from exc
    except Exception:
        incoming.unlink(missing_ok=True)
        raise

    print()
    print("SUCCESS: v3 installed")
    print("Installed:", target)
    print("Backup:", backup)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print()
        print("INSTALL FAILED:", type(exc).__name__ + ":", exc)
        raise SystemExit(1)
