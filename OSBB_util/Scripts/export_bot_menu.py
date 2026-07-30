#!/usr/bin/env python
"""
Модуль для экспорта структуры меню Telegram-бота.
Может использоваться как самостоятельный скрипт или импортироваться.

Пример запуска из командной строки:
  python export_bot_menu.py --bot G:/Programming/OSBB_cl/Bots/parking_bot.py --output ./snapshots

Пример импорта в другой модуль:
  from export_bot_menu import export_bot_menu
  export_bot_menu(bot_file=Path("..."), snapshots_root=Path("..."))
"""

import sys
import argparse
import re
import ast
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Set

# ==========================================
# КОНФИГУРАЦИЯ (по умолчанию)
# ==========================================

DEFAULT_BOT_FILE = Path("G:/Programming/OSBB_cl/Bots/parking_bot.py")
DEFAULT_SNAPSHOTS_DIR = Path("G:/Programming/Py/OSBB_util/snapshots")


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_project_name(bot_file: Path) -> str:
    """Возвращает имя проекта по пути к файлу бота"""
    return bot_file.parent.parent.name


def get_snapshot_dir(bot_file: Path, snapshots_root: Path) -> Path:
    """Формирует путь к каталогу снимка с датой"""
    project_name = get_project_name(bot_file)
    date_str = datetime.now().strftime("%Y_%m_%d")
    return snapshots_root / f"{date_str}_{project_name}"


# ==========================================
# ОСНОВНАЯ ЛОГИКА
# ==========================================

def extract_menus(content: str) -> Dict[str, List[List[str]]]:
    """Извлекает все меню (списки кнопок) из кода"""
    menus = {}
    
    # Ищем переменные с кнопками
    patterns = [
        r'([A-Z_]+_MENU)\s*=\s*\[([^\]]+)\]',  # *_MENU = [ ... ]
        r'([A-Z_]+_KEYBOARD)\s*=\s*\[([^\]]+)\]',  # *_KEYBOARD = [ ... ]
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            name = match.group(1)
            items = match.group(2)
            
            # Разбираем кнопки
            buttons = []
            for line in items.split('\n'):
                line = line.strip()
                if not line:
                    continue
                # Ищем строки в кавычках
                found = re.findall(r'["\']([^"\']+)["\']', line)
                if found:
                    # Убираем эмодзи для чистоты
                    clean = []
                    for btn in found:
                        clean_btn = re.sub(r'[^\w\s\-\.\(\)]', '', btn)
                        clean.append(clean_btn.strip())
                    buttons.append(clean)
            
            if buttons:
                menus[name] = buttons
    
    return menus


def extract_handlers(content: str) -> Dict[str, str]:
    """Извлекает обработчики (async def handle_*)"""
    handlers = {}
    pattern = r'async\s+def\s+(handle_\w+)\s*\([^)]*\)\s*:\s*"""(.*?)"""'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        name = match.group(1)
        doc = match.group(2).strip()
        handlers[name] = doc
    
    return handlers


def extract_states(content: str) -> Set[str]:
    """Извлекает состояния пользователя (user_states)"""
    states = set()
    
    # Ищем строки вида user_states[...] = "..."
    pattern = r'user_states\[[^\]]+\]\s*=\s*(["\'])([^"\']+)\1'
    for match in re.finditer(pattern, content):
        states.add(match.group(2))
    
    # Ищем кортежи состояний
    pattern2 = r'user_states\[[^\]]+\]\s*=\s*\(\s*(["\'])([^"\']+)\1\s*,'
    for match in re.finditer(pattern2, content):
        states.add(match.group(2))
    
    return states


def extract_access_checks(content: str) -> Set[str]:
    """Извлекает проверки доступа"""
    patterns = [
        r'is_admin_user\s*\([^)]*\)',
        r'has_guard_workspace_access\s*\([^)]*\)',
        r'has_service_workspace_access\s*\([^)]*\)',
        r'SUPER_ADMIN_IDS',
        r'ADMIN_IDS',
    ]
    
    checks = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            checks.add(match.group(0))
    
    return checks


def export_bot_menu(
    bot_file: Path,
    snapshots_root: Optional[Path] = None,
) -> Path:
    """
    Экспортирует структуру меню Telegram-бота в папку с датой внутри snapshots/.
    
    Args:
        bot_file: путь к файлу бота
        snapshots_root: корневой каталог для снимков
    
    Returns:
        Path: путь к созданному каталогу снимка
    """
    if snapshots_root is None:
        snapshots_root = DEFAULT_SNAPSHOTS_DIR
    
    output_dir = get_snapshot_dir(bot_file, snapshots_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not bot_file.exists():
        print(f"⚠️ Файл бота не найден: {bot_file}")
        return output_dir
    
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Извлекаем данные
    menus = extract_menus(content)
    handlers = extract_handlers(content)
    states = extract_states(content)
    access_checks = extract_access_checks(content)
    
    # 1. Структура меню (TXT)
    structure_file = output_dir / "bot_menu_structure.txt"
    with open(structure_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("🤖 СТРУКТУРА МЕНЮ TELEGRAM-БОТА\n")
        f.write("="*80 + "\n")
        f.write(f"Файл: {bot_file.name}\n")
        f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Меню
        f.write("📋 СПИСОК МЕНЮ\n")
        f.write("-"*80 + "\n\n")
        for menu_name, buttons in sorted(menus.items()):
            f.write(f"📌 {menu_name}\n")
            f.write("-"*40 + "\n")
            for row in buttons:
                f.write(f"  • {' | '.join(row)}\n")
            f.write("\n")
        
        # Состояния
        if states:
            f.write("📌 СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЯ\n")
            f.write("-"*80 + "\n\n")
            for state in sorted(states):
                f.write(f"  • {state}\n")
            f.write("\n")
        
        # Проверки доступа
        if access_checks:
            f.write("🔐 ПРОВЕРКИ ДОСТУПА\n")
            f.write("-"*80 + "\n\n")
            for check in sorted(access_checks):
                f.write(f"  • {check}\n")
            f.write("\n")
        
        # Обработчики
        if handlers:
            f.write("🎯 ОБРАБОТЧИКИ\n")
            f.write("-"*80 + "\n\n")
            for handler, doc in sorted(handlers.items()):
                f.write(f"  • {handler}\n")
                if doc:
                    f.write(f"      {doc}\n")
            f.write("\n")
    
    print(f"  ✅ bot_menu_structure.txt")
    
    # 2. Markdown-версия
    md_file = output_dir / "bot_menu.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 🤖 Структура меню Telegram-бота\n\n")
        f.write(f"**Файл:** `{bot_file.name}`  \n")
        f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # Меню
        f.write("## 📋 Список меню\n\n")
        for menu_name, buttons in sorted(menus.items()):
            f.write(f"### `{menu_name}`\n\n")
            f.write("```\n")
            for row in buttons:
                f.write(f"{' | '.join(row)}\n")
            f.write("```\n\n")
        
        # Состояния
        if states:
            f.write("## 📌 Состояния пользователя\n\n")
            f.write("```\n")
            for state in sorted(states):
                f.write(f"{state}\n")
            f.write("```\n\n")
        
        # Обработчики
        if handlers:
            f.write("## 🎯 Обработчики\n\n")
            for handler, doc in sorted(handlers.items()):
                f.write(f"### `{handler}`\n\n")
                if doc:
                    f.write(f"{doc}\n\n")
    
    print(f"  ✅ bot_menu.md")
    
    return output_dir


# ==========================================
# КОМАНДНАЯ СТРОКА
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Экспорт структуры меню Telegram-бота")
    parser.add_argument("--bot", type=str, default=str(DEFAULT_BOT_FILE),
                       help="Путь к файлу бота")
    parser.add_argument("--snapshots", type=str, default=str(DEFAULT_SNAPSHOTS_DIR),
                       help="Корневой каталог для снимков")
    
    args = parser.parse_args()
    
    bot_file = Path(args.bot)
    snapshots_root = Path(args.snapshots)
    
    if not bot_file.exists():
        print(f"❌ Ошибка: файл бота не найден: {bot_file}")
        sys.exit(1)
    
    print(f"🤖 Экспорт структуры меню бота")
    print(f"📁 Файл: {bot_file}")
    print(f"📁 Снимок: {get_snapshot_dir(bot_file, snapshots_root)}")
    print("-" * 40)
    
    export_bot_menu(
        bot_file=bot_file,
        snapshots_root=snapshots_root,
    )
    
    print("-" * 40)
    print("✅ Готово!")


if __name__ == "__main__":
    main()