# G:\Programming\Py\OSBB_util\streamlit_apps\utils\db.py
"""
Подключение к базе данных OSBB.
Использует ГЛОБАЛЬНЫЙ config.py из OSBB_cl.
"""

import sys
import sqlite3
from pathlib import Path

# ==========================================
# ПУТЬ К КОРНЮ ПРОЕКТА OSBB_cl
# ==========================================
# db.py лежит в: OSBB_util/streamlit_apps/utils/db.py
# Поднимаемся на 2 уровня до OSBB_util, потом на 1 до Py, потом в OSBB_cl

UTIL_ROOT = Path(__file__).resolve().parent.parent.parent  # OSBB_util/
PY_ROOT = UTIL_ROOT.parent  # Py/
PROJECT_ROOT = PY_ROOT.parent / "OSBB_cl"  # G:/Programming/OSBB_cl

sys.path.insert(0, str(PROJECT_ROOT))

from config import paths, USE_TEST_DB


def get_conn():
    """Возвращает соединение с БД"""
    db_path = paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def get_db_path() -> Path:
    """Возвращает путь к текущей БД"""
    return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE


def get_connection_info() -> dict:
    """Информация о подключении"""
    db_path = get_db_path()
    return {
        "path": str(db_path),
        "exists": db_path.exists(),
        "size_mb": round(db_path.stat().st_size / (1024 * 1024), 2) if db_path.exists() else 0,
        "mode": "TEST" if USE_TEST_DB else "PRODUCTION",
    }