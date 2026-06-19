# config.py (в корне Py/)
import sys
from pathlib import Path
import platform

# Добавляем корень Py/ в путь поиска модулей
PY_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PY_ROOT))

import subprocess
import re
import json
from datetime import datetime

# ==================================================
# ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ==================================================

# USE_TEST_DB = True
USE_TEST_DB = False

class ProjectPaths:
    def __init__(self, project_root=None):
        self.os_name = platform.system()
        self.home = Path.home()

        # ==================================================
        # ДИСКИ И ОСНОВНЫЕ КАТАЛОГИ
        # ==================================================
        if self.os_name == "Windows":
            self.EXTERNAL_DRIVE = Path("D:/")
            self.ONEDRIVE = self._get_onedrive_path()
            # "D:\OneDrive\Flat_Arn.xlsx"
        elif self.os_name == "Darwin":
            self.EXTERNAL_DRIVE = Path("/Volumes/microSD256")
            self.ONEDRIVE = self._get_onedrive_path()
        else:
            self.EXTERNAL_DRIVE = Path("/mnt/external")
            self.ONEDRIVE = self.home / "OneDrive"  # fallback

        if project_root:
            self.PROJECT_ROOT = Path(project_root).resolve()
        else:
            self.PROJECT_ROOT = Path.cwd()

        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.inp_dir = str(self.ONEDRIVE)

        # ==================================================
        # СЕКРЕТЫ
        # ==================================================
        if self.os_name == "Windows":
            self.SECRETS_DIR = Path("G:/Prog_secret")
        else:
            self.SECRETS_DIR = self.home / "Programming" / "Secrets"

        self.TELEGRAM_SECRETS_FILE = self.SECRETS_DIR / "telegram_osbb.py"

        # ==================================================
        # ПРОЕКТ MUSIC
        # ==================================================
        self.BASE_MUSIC_DIR = self.EXTERNAL_DRIVE / "Music" / "fav"
        self.TMP_DIR = self.BASE_MUSIC_DIR / "tmp"
        self.LOG_DIR = self.BASE_MUSIC_DIR / "log"

        # ==================================================
        # ПРОЕКТ FLAT (отчёты по квартире)
        # ==================================================
        self.FLAT_FILE = self.ONEDRIVE / "Flat_Arn.xlsx"
        self.DOCUMENTS = self.ONEDRIVE / "Документы"

        # ==================================================
        # ПРОЕКТ OSBB
        # ==================================================
        self.OSBB_ROOT = PY_ROOT / "OSBB"
        self.OSBB_DATA_DIR = self.OSBB_ROOT / "Data"
        self.OSBB_RAW_DIR = self.OSBB_DATA_DIR / "raw"
        self.OSBB_TYPED_DIR = self.OSBB_RAW_DIR / "typed"
        self.OSBB_DB_DIR = self.OSBB_DATA_DIR / "db"
        self.OSBB_EXPORTS_DIR = self.OSBB_DATA_DIR / "exports"
        self.OSBB_LOGS_DIR = self.OSBB_DATA_DIR / "logs"
        self.OSBB_BACKUPS_DIR = self.OSBB_DB_DIR / "backups"

        self.OSBB_DB_FILE = self.OSBB_DB_DIR / "osbb.db"
        self.OSBB_TEST_DB_FILE = self.OSBB_DB_DIR / "osbb_test.db"

        self.OSBB_HOUSE_REGISTRY_FILE = (
            self.OSBB_DATA_DIR / "24А ПОЛНЫЙ СПИСОК Сервис Житлобуд1 - Copy.xlsx"
        )
        self.OSBB_PAPER_PARKING_FILE = (
            self.OSBB_TYPED_DIR / "OSBB_Base_Cleaned_06_06.xlsx"
        )
        self.OSBB_TBOT_PARKING_FILE = (
            self.OSBB_TYPED_DIR / "parking_tbot2.xlsx"
        )
        self.OSBB_AUDIT_REPORT_FILE = (
            self.OSBB_TYPED_DIR / "DATABASE_AUDIT_REPORT_06_06.txt"
        )
        self.OSBB_QUARANTINE_DB_FILE = self.OSBB_DB_DIR / "osbb_quarantine.db"
        self.OSBB_TELEGRAM_DB_FILE = self.OSBB_DB_DIR / "osbb_telegram.db"
        self.OSBB_TELEGRAM_RAW_DIR = self.OSBB_RAW_DIR / "telegram"

    # ==================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ==================================================
    def _get_onedrive_path(self):
        if self.os_name == "Windows":
            return Path("D:/OneDrive")
        else:
            return self.home / "Library/CloudStorage/OneDrive-Personal"

    def get_season_folder(self):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if 3 <= month <= 5:
            return f"{year}_spring"
        elif 6 <= month <= 8:
            return f"{year}_summer"
        elif (9 <= month <= 11) or (month == 12 and day <= 14):
            return f"{year}_autumn"
        else:
            if month == 12 and day >= 15:
                return f"{year + 1}_winter"
            else:
                return f"{year}_winter"

    def get_current_season_dir(self):
        return self.BASE_MUSIC_DIR / self.get_season_folder()

    def get_log_file(self):
        today = datetime.now().strftime("%Y%m%d")
        return self.LOG_DIR / f"download_{today}.txt"

    def ensure_directories(self):
        dirs = [
            self.get_current_season_dir(),
            self.TMP_DIR,
            self.LOG_DIR,
            self.OSBB_DATA_DIR,
            self.OSBB_RAW_DIR,
            self.OSBB_TYPED_DIR,
            self.OSBB_DB_DIR,
            self.OSBB_EXPORTS_DIR,
            self.OSBB_LOGS_DIR,
            self.OSBB_BACKUPS_DIR,
            self.OSBB_TELEGRAM_RAW_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return self.get_current_season_dir()

# ✅ ЕДИНЫЙ ЭКЗЕМПЛЯР ДЛЯ ВСЕХ МОДУЛЕЙ
paths = ProjectPaths()