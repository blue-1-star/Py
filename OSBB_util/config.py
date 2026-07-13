# G:\Programming\Py\OSBB_util\local_config.py
"""
ЛОКАЛЬНЫЙ конфиг для утилитарного проекта OSBB_util
НАСЛЕДУЕТ пути из ГЛОБАЛЬНОГО config.py (в корне Py/)

ВНИМАНИЕ: 
- config.py (глобальный) — в G:\Programming\Py\
- local_config.py (локальный) — в G:\Programming\Py\OSBB_util\
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем корень Py/ в путь (чтобы импортировать глобальный config)
PY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PY_ROOT))

# Импортируем ГЛОБАЛЬНЫЙ config
from config import paths, USE_TEST_DB


class UtilConfig:
    """
    Локальная конфигурация для утилитарного проекта
    Использует пути из глобального config.py
    """
    
    def __init__(self):
        # ==================================================
        # КОРНЕВЫЕ ПУТИ (из глобального config)
        # ==================================================
        self.py_root = PY_ROOT
        self.osbb_root = paths.OSBB_ROOT
        
        # ==================================================
        # ПУТИ УТИЛИТАРНОГО ПРОЕКТА
        # ==================================================
        self.util_root = PY_ROOT / "OSBB_util"
        self.scripts_dir = self.util_root / "scripts"
        self.modules_dir = self.util_root / "modules"
        self.output_dir = self.util_root / "output"
        self.templates_dir = self.util_root / "templates"
        self.data_dir = self.util_root / "data"
        self.logs_dir = self.util_root / "logs"
        
        # ==================================================
        # ПОДКАТАЛОГИ OUTPUT
        # ==================================================
        self.tree_dir = self.output_dir / "01_project_tree"
        self.db_dir = self.output_dir / "02_database"
        self.tables_dir = self.db_dir / "tables"
        self.code_dir = self.output_dir / "03_code_analysis"
        self.api_dir = self.output_dir / "04_api_docs"
        self.reports_dir = self.output_dir / "05_reports"
        self.archive_dir = self.output_dir / "06_archive"
        
        # ==================================================
        # ПУТИ К БАЗАМ ДАННЫХ (из глобального config)
        # ==================================================
        self.db_test = paths.OSBB_TEST_DB_FILE
        self.db_main = paths.OSBB_DB_FILE
        self.use_test_db = USE_TEST_DB
        
        # ==================================================
        # НАСТРОЙКИ
        # ==================================================
        self.app_name = "OSBB Utilities"
        self.version = "0.1.0"
        
        # Создаем все директории
        self.ensure_directories()
    
    def ensure_directories(self):
        """Создает все необходимые директории"""
        dirs = [
            self.util_root,
            self.scripts_dir,
            self.modules_dir,
            self.output_dir,
            self.templates_dir,
            self.data_dir,
            self.logs_dir,
            self.tree_dir,
            self.db_dir,
            self.tables_dir,
            self.code_dir,
            self.api_dir,
            self.reports_dir,
            self.archive_dir,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def get_timestamp(self) -> str:
        """Возвращает текущий timestamp для имен файлов"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_archive_dir(self) -> Path:
        """Создает и возвращает путь к архиву с текущей датой"""
        timestamp = self.get_timestamp()
        archive_path = self.archive_dir / timestamp
        archive_path.mkdir(parents=True, exist_ok=True)
        return archive_path


# ==================================================
# ЕДИНСТВЕННЫЙ ЭКЗЕМПЛЯР
# ==================================================

# Создаем глобальный экземпляр локального конфига
local_config = UtilConfig()