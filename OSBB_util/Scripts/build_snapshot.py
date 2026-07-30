#!/usr/bin/env python
"""
Главный скрипт для создания снимка состояния проекта.
Запускает все утилиты, создаёт архив и сохраняет снимок по дате.

Пример запуска:
  python build_snapshot.py --root G:/Programming/OSBB_cl
  python build_snapshot.py --root G:/Programming/OSBB_cl --no-archive
  python build_snapshot.py --root G:/Programming/OSBB_cl --sample
"""

import sys
import argparse
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Optional

# ==========================================
# КОНФИГУРАЦИЯ
# ==========================================

DEFAULT_ROOT = Path("G:/Programming/OSBB_cl")
DEFAULT_SNAPSHOTS_DIR = Path("G:/Programming/Py/OSBB_util/snapshots")


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_project_name(root_path: Path) -> str:
    """Возвращает имя проекта по имени корневого каталога"""
    return root_path.name


def get_snapshot_dir(root_path: Path, snapshots_root: Path) -> Path:
    """Формирует путь к каталогу снимка с датой и временем"""
    project_name = get_project_name(root_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return snapshots_root / f"{timestamp}_{project_name}"


def get_zip_path(snapshot_dir: Path) -> Path:
    """Формирует путь к ZIP-архиву"""
    return snapshot_dir.with_suffix(".zip")


# ==========================================
# ЗАПУСК УТИЛИТ
# ==========================================

def run_export_tree(root_path: Path, snapshot_dir: Path) -> bool:
    """Запускает export_tree.py"""
    try:
        from export_tree import export_tree
        export_tree(
            root_path=root_path,
            snapshots_root=snapshot_dir.parent,
        )
        return True
    except ImportError:
        print("⚠️ export_tree не найден, пропускаем")
        return False
    except Exception as e:
        print(f"❌ Ошибка в export_tree: {e}")
        return False


def run_export_db_schema(root_path: Path, snapshot_dir: Path, include_sample: bool = False) -> bool:
    """Запускает export_db_schema.py"""
    try:
        from export_db_schema import export_db_schema
        db_path = root_path / "data" / "db" / "osbb_test.db"
        if not db_path.exists():
            # Пробуем старую структуру
            db_path = root_path / "OSBB" / "Data" / "db" / "osbb_test.db"
        if not db_path.exists():
            print(f"⚠️ БД не найдена: {db_path}")
            return False
        export_db_schema(
            db_path=db_path,
            snapshots_root=snapshot_dir.parent,
            include_data_sample=include_sample,
        )
        return True
    except ImportError:
        print("⚠️ export_db_schema не найден, пропускаем")
        return False
    except Exception as e:
        print(f"❌ Ошибка в export_db_schema: {e}")
        return False


def run_export_bot_menu(root_path: Path, snapshot_dir: Path) -> bool:
    """Запускает export_bot_menu.py"""
    try:
        from export_bot_menu import export_bot_menu
        bot_file = root_path / "Bots" / "parking_bot.py"
        if not bot_file.exists():
            # Пробуем старую структуру
            bot_file = root_path / "OSBB" / "Bots" / "parking_bot.py"
        if not bot_file.exists():
            print(f"⚠️ Файл бота не найден: {bot_file}")
            return False
        export_bot_menu(
            bot_file=bot_file,
            snapshots_root=snapshot_dir.parent,
        )
        return True
    except ImportError:
        print("⚠️ export_bot_menu не найден, пропускаем")
        return False
    except Exception as e:
        print(f"❌ Ошибка в export_bot_menu: {e}")
        return False


# ==========================================
# СОЗДАНИЕ ИНДЕКСА И МЕТА-ФАЙЛОВ
# ==========================================

def create_index(root_path: Path, snapshot_dir: Path, results: dict) -> None:
    """Создаёт _index.md со сводкой"""
    index_path = snapshot_dir / "_index.md"
    
    content = f"""# 📊 Снимок состояния проекта

**Проект:** {get_project_name(root_path)}
**Корень:** {root_path}
**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📁 Содержание снимка

| Раздел | Описание |
|--------|----------|
| [01_project_tree](01_project_tree/) | Дерево каталогов проекта |
| [02_database](02_database/) | Структура базы данных |
| [03_bot_menu](03_bot_menu/) | Структура меню Telegram-бота |

---

## 📊 Результаты сборки

| Утилита | Статус |
|---------|--------|
| export_tree | {'✅' if results.get('tree') else '❌'} |
| export_db_schema | {'✅' if results.get('db') else '❌'} |
| export_bot_menu | {'✅' if results.get('bot') else '❌'} |

---

## 📦 Архив

Весь снимок упакован в: `{snapshot_dir.name}.zip`
"""
    
    index_path.write_text(content, encoding='utf-8')
    print(f"  ✅ _index.md")


def create_snapshot_info(root_path: Path, snapshot_dir: Path, results: dict) -> None:
    """Создаёт _snapshot_info.json с метаданными"""
    info_path = snapshot_dir / "_snapshot_info.json"
    
    info = {
        "project": {
            "name": get_project_name(root_path),
            "root": str(root_path),
        },
        "snapshot": {
            "timestamp": datetime.now().isoformat(),
            "directory": str(snapshot_dir),
        },
        "results": results,
        "utilities": {
            "export_tree": "export_tree.py",
            "export_db_schema": "export_db_schema.py",
            "export_bot_menu": "export_bot_menu.py",
        }
    }
    
    info_path.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  ✅ _snapshot_info.json")


# ==========================================
# АРХИВАЦИЯ
# ==========================================

def create_archive(snapshot_dir: Path) -> Path:
    """
    Создаёт ZIP-архив всего снимка (все папки и файлы).
    """
    zip_path = get_zip_path(snapshot_dir)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in snapshot_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(snapshot_dir.parent)
                zf.write(file_path, arcname)
    
    print(f"  ✅ Архив: {zip_path.name}")
    return zip_path


# ==========================================
# ОСНОВНАЯ ФУНКЦИЯ
# ==========================================

def build_snapshot(
    root_path: Path,
    snapshots_root: Optional[Path] = None,
    no_archive: bool = False,
    include_sample: bool = False,
) -> Path:
    """
    Создаёт полный снимок состояния проекта.
    """
    if snapshots_root is None:
        snapshots_root = DEFAULT_SNAPSHOTS_DIR
    
    snapshot_dir = get_snapshot_dir(root_path, snapshots_root)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    print("=" * 60)
    print(f"📸 СНИМОК ПРОЕКТА: {get_project_name(root_path)}")
    print("=" * 60)
    print(f"📁 Корень: {root_path}")
    print(f"📁 Снимок: {snapshot_dir}")
    print("-" * 40)
    
    # 1. Запускаем все утилиты
    print("🌳 Экспорт дерева...")
    results['tree'] = run_export_tree(root_path, snapshot_dir)
    
    print("🗄️ Экспорт БД...")
    results['db'] = run_export_db_schema(root_path, snapshot_dir, include_sample)
    
    print("🤖 Экспорт меню бота...")
    results['bot'] = run_export_bot_menu(root_path, snapshot_dir)
    
    # 2. Создаём индекс и мета-файлы
    print("📄 Создание индекса...")
    create_index(root_path, snapshot_dir, results)
    
    print("📄 Создание метаинформации...")
    create_snapshot_info(root_path, snapshot_dir, results)
    
    # 3. Архивируем (если нужно)
    if not no_archive:
        print("📦 Создание архива...")
        create_archive(snapshot_dir)
    
    print("-" * 40)
    print(f"✅ Снимок создан: {snapshot_dir}")
    
    return snapshot_dir


# ==========================================
# КОМАНДНАЯ СТРОКА
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Создание снимка состояния проекта")
    parser.add_argument("--root", type=str, default=str(DEFAULT_ROOT),
                       help="Корневой каталог проекта")
    parser.add_argument("--snapshots", type=str, default=str(DEFAULT_SNAPSHOTS_DIR),
                       help="Корневой каталог для снимков")
    parser.add_argument("--no-archive", action="store_true",
                       help="Не создавать ZIP-архив")
    parser.add_argument("--sample", action="store_true",
                       help="Включать примеры данных из БД")
    
    args = parser.parse_args()
    
    root_path = Path(args.root)
    snapshots_root = Path(args.snapshots)
    
    if not root_path.exists():
        print(f"❌ Ошибка: корневой каталог не найден: {root_path}")
        sys.exit(1)
    
    build_snapshot(
        root_path=root_path,
        snapshots_root=snapshots_root,
        no_archive=args.no_archive,
        include_sample=args.sample,
    )


if __name__ == "__main__":
    main()