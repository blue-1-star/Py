#!/usr/bin/env python
"""
Модуль для экспорта дерева каталогов проекта.
Сохраняет результат в папку с датой (dd_mm_yy) внутри snapshots/.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# ==========================================
# КОНФИГУРАЦИЯ
# ==========================================

DEFAULT_ROOT = Path("G:/Programming/Py/OSBB")
DEFAULT_SNAPSHOTS_DIR = Path("G:/Programming/Py/OSBB_util/snapshots")

EXCLUDE_DIRS = [
    "__pycache__", ".git", ".venv", "venv", "env",
    ".idea", ".vscode", "node_modules", "dist", "build",
    "*.egg-info", ".pytest_cache", ".mypy_cache"
]

EXCLUDE_FILES = [
    "*.pyc", "*.pyo", "*.so", "*.dll", "*.dylib",
    ".DS_Store", "Thumbs.db"
]


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_project_name(root_path: Path) -> str:
    """Возвращает имя проекта по имени корневого каталога"""
    return root_path.name


def get_snapshot_dir(root_path: Path, snapshots_root: Path) -> Path:
    """Формирует путь к каталогу снимка с датой"""
    project_name = get_project_name(root_path)
    date_str = datetime.now().strftime("%Y_%m_%d")
    return snapshots_root / f"{date_str}_{project_name}"


# ==========================================
# ОСНОВНАЯ ЛОГИКА
# ==========================================

def should_exclude(path: Path) -> bool:
    """Проверяет, нужно ли исключить путь"""
    name = path.name

    if path.is_dir():
        for pattern in EXCLUDE_DIRS:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern == name:
                return True
        if name.startswith(".") and name not in [".git"]:
            return True

    if path.is_file():
        for pattern in EXCLUDE_FILES:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern == name:
                return True

    return False


def generate_tree(
    path: Path,
    prefix: str = "",
    depth: int = 0,
    max_depth: Optional[int] = None,
    show_size: bool = True,
    show_date: bool = True,
) -> str:
    """Генерирует строку с деревом каталогов"""
    
    if not path.exists() or not path.is_dir():
        return ""
    
    if max_depth is not None and depth > max_depth:
        return ""
    
    lines = []
    
    try:
        items = sorted(path.iterdir())
    except PermissionError:
        return f"{prefix}└── [Нет доступа]\n"
    
    filtered = [item for item in items if not should_exclude(item)]
    
    for i, item in enumerate(filtered):
        is_last = i == len(filtered) - 1
        connector = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")
        
        line = f"{prefix}{connector}{item.name}"
        
        if item.is_file() and show_size:
            size = item.stat().st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.2f} MB"
            line += f" [{size_str}]"
            
            if show_date:
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                line += f" {mtime.strftime('%Y-%m-%d %H:%M')}"
        
        elif item.is_dir():
            line += "/"
        
        lines.append(line)
        
        if item.is_dir() and (max_depth is None or depth + 1 <= max_depth):
            sub_tree = generate_tree(
                item, next_prefix, depth + 1,
                max_depth, show_size, show_date
            )
            if sub_tree:
                lines.append(sub_tree.rstrip("\n"))
    
    return "\n".join(lines)


def export_tree(
    root_path: Path,
    snapshots_root: Optional[Path] = None,
    max_depth: Optional[int] = None,
    show_size: bool = True,
    show_date: bool = True,
    include_header: bool = True,
) -> Path:
    """
    Экспортирует дерево каталогов в папку с датой внутри snapshots/.
    
    Args:
        root_path: корневой каталог проекта
        snapshots_root: корневой каталог для снимков (по умолчанию snapshots/)
        max_depth: максимальная глубина
        show_size: показывать размер
        show_date: показывать дату
        include_header: добавить заголовок
    
    Returns:
        Path: путь к созданному каталогу снимка
    """
    if snapshots_root is None:
        snapshots_root = DEFAULT_SNAPSHOTS_DIR
    
    output_dir = get_snapshot_dir(root_path, snapshots_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    project_name = get_project_name(root_path)
    
    header = f"""
{'='*80}
ДЕРЕВО КАТАЛОГОВ ПРОЕКТА
{'='*80}
Проект:     {project_name}
Корень:     {root_path}
Дата:       {timestamp}
Глубина:    {'без ограничений' if max_depth is None else f'{max_depth} уровней'}
{'='*80}

"""
    
    tree = generate_tree(root_path, max_depth=max_depth, show_size=show_size, show_date=show_date)
    
    if include_header:
        content = header + tree
    else:
        content = tree
    
    output_file = output_dir / "tree_full.txt"
    output_file.write_text(content, encoding="utf-8")
    
    # Ограниченное дерево
    tree_limited = generate_tree(root_path, max_depth=max_depth, show_size=False, show_date=False)
    limited_file = output_dir / "tree_limited.txt"
    limited_file.write_text(tree_limited, encoding="utf-8")
    
    # Дерево по глубине
    if max_depth is None:
        for depth in [2, 3]:
            tree_depth = generate_tree(root_path, max_depth=depth, show_size=True, show_date=True)
            depth_file = output_dir / f"tree_depth_{depth}.txt"
            depth_file.write_text(tree_depth, encoding="utf-8")
    
    print(f"✅ tree_full.txt")
    print(f"✅ tree_limited.txt")
    if max_depth is None:
        print(f"✅ tree_depth_2.txt")
        print(f"✅ tree_depth_3.txt")
    
    return output_dir


# ==========================================
# КОМАНДНАЯ СТРОКА
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Экспорт дерева каталогов")
    parser.add_argument("--root", type=str, default=str(DEFAULT_ROOT),
                       help="Корневой каталог проекта")
    parser.add_argument("--snapshots", type=str, default=str(DEFAULT_SNAPSHOTS_DIR),
                       help="Корневой каталог для снимков")
    parser.add_argument("--depth", type=int, default=None,
                       help="Максимальная глубина")
    parser.add_argument("--no-size", action="store_true",
                       help="Не показывать размер")
    parser.add_argument("--no-date", action="store_true",
                       help="Не показывать дату")
    parser.add_argument("--no-header", action="store_true",
                       help="Не добавлять заголовок")
    
    args = parser.parse_args()
    
    root_path = Path(args.root)
    snapshots_root = Path(args.snapshots)
    
    if not root_path.exists():
        print(f"❌ Ошибка: корневой каталог не найден: {root_path}")
        sys.exit(1)
    
    print(f"🌳 Экспорт дерева каталогов")
    print(f"📁 Проект: {root_path.name}")
    print(f"📁 Снимок: {get_snapshot_dir(root_path, snapshots_root)}")
    print("-" * 40)
    
    export_tree(
        root_path=root_path,
        snapshots_root=snapshots_root,
        max_depth=args.depth,
        show_size=not args.no_size,
        show_date=not args.no_date,
        include_header=not args.no_header,
    )
    
    print("-" * 40)
    print("✅ Готово!")


if __name__ == "__main__":
    main()