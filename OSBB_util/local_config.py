# G:\Programming\Py\OSBB_util\config.py
"""
Локальный конфиг для утилитарного проекта OSBB_util
Наследует пути из корневого config.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем корень Py/ в путь
PY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PY_ROOT))

from config import paths, USE_TEST_DB


class UtilConfig:
    """Конфигурация для утилитарного проекта"""
    
    def __init__(self):
        # Корневые пути
        self.py_root = PY_ROOT
        self.osbb_root = paths.OSBB_ROOT
        
        # Пути к утилитам
        self.util_root = PY_ROOT / "OSBB_util"
        self.scripts_dir = self.util_root / "scripts"
        self.modules_dir = self.util_root / "modules"
        self.output_dir = self.util_root / "output"
        self.templates_dir = self.util_root / "templates"
        self.data_dir = self.util_root / "data"
        self.logs_dir = self.util_root / "logs"
        
        # Подкаталоги output
        self.tree_dir = self.output_dir / "01_project_tree"
        self.db_dir = self.output_dir / "02_database"
        self.tables_dir = self.db_dir / "tables"
        self.code_dir = self.output_dir / "03_code_analysis"
        self.api_dir = self.output_dir / "04_api_docs"
        self.reports_dir = self.output_dir / "05_reports"
        self.archive_dir = self.output_dir / "06_archive"
        
        # Пути к БД (из основного проекта)
        self.db_test = paths.OSBB_TEST_DB_FILE
        self.db_main = paths.OSBB_DB_FILE
        
        # Настройки БД
        self.use_test_db = USE_TEST_DB
        
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


# Создаем глобальный экземпляр
local_config = UtilConfig()