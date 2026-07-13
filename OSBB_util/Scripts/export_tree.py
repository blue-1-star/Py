# G:\Programming\Py\OSBB_util\scripts\export_tree.py
"""
Экспорт дерева каталогов проекта OSBB
Сохраняет в output/01_project_tree/
"""

import sys
from pathlib import Path

# Добавляем корень утилиты в путь
UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

# Импортируем ЛОКАЛЬНЫЙ конфиг
from local_config import local_config

# Импортируем модуль
from modules.tree_generator import TreeGenerator


def main():
    print("=" * 60)
    print("🌳 ЭКСПОРТ ДЕРЕВА КАТАЛОГОВ")
    print("=" * 60)
    print(f"📁 Исходный проект: {local_config.osbb_root}")
    print(f"📁 Целевой каталог: {local_config.tree_dir}")
    print("-" * 60)
    
    # Создаем генератор
    generator = TreeGenerator(
        root_path=local_config.osbb_root,
        output_dir=local_config.tree_dir
    )
    
    # Генерируем разные варианты дерева
    generator.generate_full_tree()
    generator.generate_limited_tree()
    generator.generate_by_depth(max_depth=2)
    generator.generate_by_depth(max_depth=3)
    
    print("\n✅ Готово!")
    print(f"📄 Результаты в: {local_config.tree_dir}")


if __name__ == "__main__":
    main()