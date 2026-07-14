# G:\Programming\Py\OSBB_util\scripts\build_report.py
"""
Главный скрипт для сбора всей информации о проекте
Запускает все утилиты и собирает отчет
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
    
    content = (
        "# 📊 Документация проекта OSBB\n\n"
        f"**Дата сборки:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "---\n\n"
        "## 📁 Глобальный vs Локальный\n\n"
        "| Файл | Расположение | Назначение |\n"
        "|------|--------------|------------|\n"
        "| `config.py` | `G:/Programming/Py/` | **ГЛОБАЛЬНЫЙ** — для всего 프로екта |\n"
        "| `local_config.py` | `G:/Programming/Py/OSBB_util/` | **ЛОКАЛЬНЫЙ** — только для утилит |\n\n"
        "---\n\n"
        "## 📁 Структура документации\n\n"
        "### [01_project_tree](01_project_tree/)\n"
        "Дерево каталогов проекта:\n"
        "- [Полное дерево](01_project_tree/tree_full.txt) — все файлы с размерами и датами\n"
        "- [Ограниченное дерево](01_project_tree/tree_limited.txt) — только структура\n"
        "- [По глубине 2](01_project_tree/tree_depth_2.txt) — первые 2 уровня\n"
        "- [По глубине 3](01_project_tree/tree_depth_3.txt) — первые 3 уровня\n\n"
        "### [02_database](02_database/)\n"
        "Документация базы данных:\n"
        "- [Полная схема SQL](02_database/schema_full.sql) — CREATE TABLE\n"
        "- [Сводная информация](02_database/schema_summary.txt) — список таблиц, связи\n"
        "- [Связи между таблицами](02_database/relationships.txt) — внешние ключи\n"
        "- [Документация таблиц](02_database/tables/) — по каждой таблице\n\n"
        "### [03_code_analysis](03_code_analysis/)\n"
        "Анализ кода (в разработке)\n\n"
        "### [04_api_docs](04_api_docs/)\n"
        "Документация API (в разработке)\n\n"
        "### [05_reports](05_reports/)\n"
        "Отчеты и анализ (в разработке)\n\n"
        "### [06_archive](06_archive/)\n"
        "Архив предыдущих версий\n\n"
        "---\n\n"
        "## 🚀 Как обновить документацию\n\n"
        "```bash\n"
        "cd G:/Programming/Py/OSBB_util\n"
        "python scripts/build_report.py\n"
        "```\n"
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Создан индекс: {index_path}")


def main():
    print("=" * 70)
    print("📊 СБОРКА ДОКУМЕНТАЦИИ ПРОЕКТА OSBB")
    print("=" * 70)
    print(f"📁 Проект: {local_config.osbb_root}")
    print(f"📁 Результат: {local_config.output_dir}")
    print("-" * 70)
    
    # Список скриптов для запуска
    scripts = [
        "export_tree.py",
        "export_db_schema.py",
    ]
    
    for script in scripts:
        run_script(script)
        print()
    
    # Создаем индекс
    create_index()
    
    print("\n" + "=" * 70)
    print("✅ ДОКУМЕНТАЦИЯ СОБРАНА!")
    print(f"📄 Откройте: {local_config.output_dir / '_index.md'}")
    print("=" * 70)


if __name__ == "__main__":
    main()