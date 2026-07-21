# -*- coding: utf-8 -*-
r"""
Apply the simplified paid-preorder workflow only to the dedicated live-services
sandbox database. It does not touch osbb.db or other sandbox files.

This migration must be launched from G:\Programming\Py\OSBB\.
The project configuration module lives one directory above OSBB
(G:\Programming\Py\config.py), as in the ordinary bot launcher.
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOTS = ROOT / "Bots"
PY_ROOT = ROOT.parent
SANDBOX = (
    ROOT
    / "Data"
    / "db"
    / "sandbox"
    / "osbb_test_live_services_2026-06-26_20-13-26.db"
)
BACKUPS = ROOT / "Data" / "db" / "sandbox" / "backups"
LOGS = ROOT / "Data" / "db" / "logs"


def _prepare_import_paths() -> None:
    """Match the normal bot launcher's Python search path."""
    for folder in (ROOT, BOTS, PY_ROOT):
        folder_text = str(folder)
        if folder_text not in sys.path:
            sys.path.insert(0, folder_text)


def _load_schema_migrator():
    """
    Load the migration logic before touching the database.

    service_preorders_core imports service_orders_core; that core imports
    config from the parent Python project directory, not from OSBB itself.
    """
    _prepare_import_paths()

    try:
        import config
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Не найден модуль config. Ожидался файл "
            f"{PY_ROOT / 'config.py'}. "
            "Проверьте, что данный файл миграции лежит прямо в "
            "G:\\Programming\\Py\\OSBB\\."
        ) from exc

    config_file = getattr(config, "__file__", None)
    if not config_file:
        raise RuntimeError("Модуль config загружен без известного файла.")

    try:
        from service_preorders_core import ensure_simplified_service_schema
    except Exception as exc:
        raise RuntimeError(
            "Не удалось загрузить service_preorders_core.py. "
            "Убедитесь, что этот файл из архива лежит прямо в "
            "G:\\Programming\\Py\\OSBB\\."
        ) from exc

    return ensure_simplified_service_schema, Path(config_file).resolve()


def _write_log(stamp: str, lines: list[str]) -> Path:
    LOGS.mkdir(parents=True, exist_ok=True)
    log = LOGS / f"simplified_services_migration_{stamp}.txt"
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log


def main() -> int:
    print("OSBB simplified paid-preorder workflow migration — corrected launcher")
    print("Project:", ROOT)
    print("Sandbox:", SANDBOX)

    if not SANDBOX.is_file():
        raise FileNotFoundError(
            "Live-services sandbox DB was not found:\n"
            f"  {SANDBOX}"
        )

    # An import/configuration failure must not create a backup or alter a DB.
    ensure_schema, config_file = _load_schema_migrator()
    print("Config:", config_file)

    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BACKUPS / (
        f"{SANDBOX.stem}_before_simplified_services_{stamp}{SANDBOX.suffix}"
    )
    shutil.copy2(SANDBOX, backup)
    print("Backup:", backup)

    conn = sqlite3.connect(SANDBOX)
    # service_preorders_core converts selected rows to dictionaries.
    # The migration connection must therefore return named SQLite rows.
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("BEGIN IMMEDIATE")
        changes = ensure_schema(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    log_lines = [
        "Simplified services sandbox migration",
        f"Project: {ROOT}",
        f"Sandbox: {SANDBOX}",
        f"Backup: {backup}",
        f"Config: {config_file}",
        *list(changes or ["Schema already up to date."]),
    ]
    log = _write_log(stamp, log_lines)

    print("Changes:")
    for line in changes or ["Schema already up to date."]:
        print(" -", line)
    print("Log:", log)
    print("MIGRATION COMPLETED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("MIGRATION FAILED:", type(exc).__name__ + ":", exc)
        traceback.print_exc()
        raise SystemExit(1)
