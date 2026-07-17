#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assistant.py
OSBB Utility Assistant v0.1

Первая версия.
Пока ничего не изменяет.
Только проверяет окружение проекта.
"""

from pathlib import Path
import sys

ROOT = Path(r"G:\Programming\Py")

FILES = {
    "Git repository": ROOT / ".git",
    "cashier_v2_ui.py": ROOT / "OSBB" / "tools" / "cashier_v2_telegram" / "cashier_v2_ui.py",
    "cashier_card.py": ROOT / "OSBB" / "tools" / "cashier_v2_telegram" / "cashier_card.py",
}


def ok(message: str):
    print(f"[ OK ] {message}")


def fail(message: str):
    print(f"[ERROR] {message}")
    sys.exit(1)


def main():

    print("=" * 60)
    print("OSBB Assistant v0.1")
    print("=" * 60)
    print(f"Project : {ROOT}")
    print()

    if not ROOT.exists():
        fail(f"Project directory not found:\n{ROOT}")

    ok("Project directory found")

    for title, path in FILES.items():

        if not path.exists():
            fail(f"{title} not found:\n{path}")

        ok(title)

    print()
    print("Environment check completed successfully.")
    print("Ready.")


if __name__ == "__main__":
    main()