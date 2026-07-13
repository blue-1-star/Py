# G:\Programming\Py\OSBB_util\Scripts\build_report.py
"""
Главный скрипт для сбора всей информации о проекте
"""

import sys
from pathlib import Path
from datetime import datetime
import subprocess

UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

from local_config import local_config


def run_script(script_name: str) -> bool:
    """Запускает скрипт и возвращает результат"""
    script_path = local_config.scripts_dir / script_name
    if not script_path.exists():
        print(f"⚠️  Скрипт не найден: {script_path}")
        return False
    
    print(f"▶️  Запуск: {script_name}")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(local_config.util_root)
        )
        if result.returncode == 0:
            print(f"   ✅ {script_name} завершен")
            return True
        else:
            print(f"   ❌ Ошибка в {script_name}")
            if result.stderr:
                print(result.stderr[:500])
            return False
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
        return False


def create_index():
    """Создает главную страницу документации"""
    index_path = local_config.output_dir / "_index.md"
    
    content = f"""
# 📊 Документация проекта OSBB

**Дата сборки:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📁 Глобальный vs Локальный

| Файл | Расположение | Назначение |
|------|--------------|------------|
| `config.py` | `G:/Programming/Py/` | **ГЛОБАЛЬНЫЙ** — для всего проекта |
| `local_config.py` | `G:/Programming/Py/OSBB_util/` | **ЛОКАЛЬНЫЙ** — только для утилит |

---

## 📁 Структура документации

### [01_project_tree](01_project_tree/)
Дерево каталогов проекта:
- [Полное дерево](01_project_tree/tree_full.txt) — все файлы с размерами и датами
- [Ограниченное дерево](01_project_tree/tree_limited.txt) — только структура
- [По глубине 2](01_project_tree/tree_depth_2.txt) — первые 2 уровня
- [По глубине 3](01_project_tree/tree_depth_3.txt) — первые 3 уровня

### [02_database](02_database/)
Документация базы данных:
- [Полная схема SQL](02_database/schema_full.sql) — CREATE TABLE для всех таблиц
- [Сводная информация](02_database/schema_summary.txt) — список таблиц, связи
- [Связи между таблицами](02_database/relationships.txt) — внешние ключи
- [Документация таблиц](02_database/tables/) — по каждой таблице отдельно

### [03_code_analysis](03_code_analysis/)
Анализ кода (в разработке)

### [04_api_docs](04_api_docs/)
Документация API (в разработке)

### [05_reports](05_reports/)
Отчеты и анализ (в разработке)

### [06_archive](06_archive/)
Архив предыдущих версий

---

## 🚀 Как обновить документацию

```bash
cd G:/Programming/Py/OSBB_util
python Scripts/build_report.py