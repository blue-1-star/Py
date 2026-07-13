# G:\Programming\Py\OSBB_util\Scripts\export_bot_menu.py
"""
Экспорт структуры меню Telegram-бота из кода parking_bot.py
Анализирует:
- Кнопки меню
- Обработчики
- Состояния
- Доступы (admin, guard, service_operator)

Сохраняет в output/04_bot_docs/
"""

import sys
import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
import json

# Добавляем корень утилиты в путь
UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

from local_config import local_config


class BotMenuExporter:
    """Экспорт структуры меню Telegram-бота"""
    
    def __init__(self, bot_file: Path, output_dir: Path):
        self.bot_file = bot_file
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Данные для анализа
        self.menus = {}           # Все меню (кнопки)
        self.handlers = {}        # Обработчики
        self.states = []          # Состояния
        self.access_checks = []   # Проверки доступа
        self.keyboards = {}       # Клавиатуры
        
    def parse_file(self) -> bool:
        """Парсит файл бота"""
        if not self.bot_file.exists():
            print(f"❌ Файл не найден: {self.bot_file}")
            return False
        
        with open(self.bot_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Парсим AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"❌ Ошибка синтаксиса: {e}")
            return False
        
        # Собираем информацию
        self._collect_menus(content)
        self._collect_keyboards(content)
        self._collect_states(content)
        self._collect_access_checks(content)
        self._collect_handlers(content)
        
        return True
    
    def _collect_menus(self, content: str):
        """Собирает все меню (списки кнопок)"""
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
                            # Убираем эмодзи
                            clean_btn = re.sub(r'[^\w\s\-\.\(\)]', '', btn)
                            clean.append(clean_btn.strip())
                        buttons.append(clean)
                
                if buttons:
                    self.menus[name] = buttons
    
    def _collect_keyboards(self, content: str):
        """Собирает функции клавиатур"""
        # Ищем функции kb() и build_number_keyboard()
        patterns = [
            r'def\s+(kb|build_number_keyboard)\s*\([^)]*\)\s*:[^}]*?return\s+([^\n;]+)',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                func_name = match.group(1)
                return_stmt = match.group(2)
                self.keyboards[func_name] = return_stmt.strip()
    
    def _collect_states(self, content: str):
        """Собирает состояния пользователя"""
        # Ищем user_states
        pattern = r'user_states\[[^\]]+\]\s*=\s*(["\'])([^"\']+)\1'
        
        states = set()
        for match in re.finditer(pattern, content):
            states.add(match.group(2))
        
        # Ищем кортежи состояний
        pattern2 = r'user_states\[[^\]]+\]\s*=\s*\(\s*(["\'])([^"\']+)\1\s*,'
        for match in re.finditer(pattern2, content):
            states.add(match.group(2))
        
        self.states = sorted(list(states))
    
    def _collect_access_checks(self, content: str):
        """Собирает проверки доступа"""
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
        
        self.access_checks = sorted(list(checks))
    
    def _collect_handlers(self, content: str):
        """Собирает обработчики"""
        # Ищем async def handle_*
        pattern = r'async\s+def\s+(handle_\w+)\s*\([^)]*\)\s*:'
        
        handlers = {}
        for match in re.finditer(pattern, content):
            name = match.group(1)
            # Ищем docstring
            doc_match = re.search(
                rf'async\s+def\s+{name}\s*\([^)]*\)\s*:\s*"""(.*?)"""',
                content,
                re.DOTALL
            )
            doc = doc_match.group(1).strip() if doc_match else ""
            handlers[name] = doc
        
        self.handlers = handlers
    
    def export_structure(self) -> Path:
        """Экспортирует структуру меню в TXT"""
        output_path = self.output_dir / "bot_menu_structure.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("🤖 СТРУКТУРА МЕНЮ TELEGRAM-БОТА\n")
            f.write("="*80 + "\n")
            f.write(f"Файл: {self.bot_file.name}\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # 1. Меню
            f.write("📋 СПИСОК МЕНЮ\n")
            f.write("-"*80 + "\n\n")
            
            for menu_name, buttons in sorted(self.menus.items()):
                f.write(f"📌 {menu_name}\n")
                f.write("-"*40 + "\n")
                for row in buttons:
                    f.write(f"  • {' | '.join(row)}\n")
                f.write("\n")
            
            # 2. Состояния
            if self.states:
                f.write("📌 СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЯ\n")
                f.write("-"*80 + "\n\n")
                for state in self.states:
                    f.write(f"  • {state}\n")
                f.write("\n")
            
            # 3. Проверки доступа
            if self.access_checks:
                f.write("🔐 ПРОВЕРКИ ДОСТУПА\n")
                f.write("-"*80 + "\n\n")
                for check in self.access_checks:
                    f.write(f"  • {check}\n")
                f.write("\n")
            
            # 4. Обработчики
            if self.handlers:
                f.write("🎯 ОБРАБОТЧИКИ\n")
                f.write("-"*80 + "\n\n")
                for handler, doc in sorted(self.handlers.items()):
                    f.write(f"  • {handler}\n")
                    if doc:
                        f.write(f"      {doc}\n")
                f.write("\n")
        
        print(f"  ✅ {output_path.name}")
        return output_path
    
    def export_menu_tree(self) -> Path:
        """Экспортирует древовидную структуру меню"""
        output_path = self.output_dir / "bot_menu_tree.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("🌳 ДЕРЕВО МЕНЮ TELEGRAM-БОТА\n")
            f.write("="*80 + "\n\n")
            
            # Строим дерево из меню
            # Главные меню
            main_menus = {
                'ADMIN_MENU': '🔐 Админ-меню',
                'CLIENT_MENU_RU': '👤 Клиентское меню',
                'USERS_MENU': '👥 Пользователи',
                'APARTMENT_MENU': '🏠 Квартира',
                'VEHICLE_REVIEW_MENU': '🚗 Автомобили',
                'VEHICLE_ACTION_MENU': '🚗 Действия с авто',
                'VEHICLE_EDIT_MENU': '✏️ Редактирование авто',
                'VEHICLE_STATUS_MENU': '📊 Статус авто',
                'CONFIRM_APARTMENT_MENU': '✅ Подтверждение квартиры',
                'USER_VERIFY_MENU': '🔎 Проверка пользователя',
            }
            
            # Связи между меню
            links = {
                'ADMIN_MENU': ['USERS_MENU', 'VEHICLE_REVIEW_MENU', 'APARTMENT_MENU'],
                'USERS_MENU': ['USER_VERIFY_MENU'],
                'APARTMENT_MENU': ['VEHICLE_REVIEW_MENU'],
                'VEHICLE_REVIEW_MENU': ['VEHICLE_ACTION_MENU', 'VEHICLE_STATUS_MENU'],
                'VEHICLE_ACTION_MENU': ['VEHICLE_EDIT_MENU'],
            }
            
            # Рисуем дерево
            def print_menu_tree(menu_name, prefix="", visited=None):
                if visited is None:
                    visited = set()
                
                if menu_name in visited:
                    return
                visited.add(menu_name)
                
                display_name = main_menus.get(menu_name, menu_name)
                f.write(f"{prefix}├── {display_name}\n")
                
                # Показываем кнопки
                if menu_name in self.menus:
                    for row in self.menus[menu_name][:3]:
                        f.write(f"{prefix}│   ├── {' | '.join(row)}\n")
                    if len(self.menus[menu_name]) > 3:
                        f.write(f"{prefix}│   └── ... и еще {len(self.menus[menu_name]) - 3} строк\n")
                
                # Переходы
                if menu_name in links:
                    new_prefix = prefix + "│   "
                    for child in links[menu_name]:
                        print_menu_tree(child, new_prefix, visited)
            
            f.write("🏠 ГЛАВНЫЙ МЕНЮ\n")
            f.write("-"*40 + "\n")
            
            # Строим дерево от корня
            print_menu_tree('ADMIN_MENU', "    ")
            print_menu_tree('CLIENT_MENU_RU', "    ")
            
            # Схема переходов
            f.write("\n" + "="*80 + "\n")
            f.write("🔗 СХЕМА ПЕРЕХОДОВ\n")
            f.write("-"*80 + "\n\n")
            for parent, children in links.items():
                parent_name = main_menus.get(parent, parent)
                f.write(f"📌 {parent_name}\n")
                for child in children:
                    child_name = main_menus.get(child, child)
                    f.write(f"  └── {child_name}\n")
                f.write("\n")
        
        print(f"  ✅ {output_path.name}")
        return output_path
    
    def export_markdown(self) -> Path:
        """Экспортирует в Markdown для документации"""
        output_path = self.output_dir / "bot_menu.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 🤖 Структура меню Telegram-бота\n\n")
            f.write(f"**Файл:** `{self.bot_file.name}`  \n")
            f.write(f"**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("---\n\n")
            
            # Все меню
            f.write("## 📋 Список меню\n\n")
            for menu_name, buttons in sorted(self.menus.items()):
                f.write(f"### `{menu_name}`\n\n")
                f.write("```\n")
                for row in buttons:
                    f.write(f"{' | '.join(row)}\n")
                f.write("```\n\n")
            
            # Состояния
            if self.states:
                f.write("## 📌 Состояния пользователя\n\n")
                f.write("```\n")
                for state in self.states:
                    f.write(f"{state}\n")
                f.write("```\n\n")
            
            # Обработчики
            if self.handlers:
                f.write("## 🎯 Обработчики\n\n")
                for handler, doc in sorted(self.handlers.items()):
                    f.write(f"### `{handler}`\n\n")
                    if doc:
                        f.write(f"{doc}\n\n")
        
        print(f"  ✅ {output_path.name}")
        return output_path
    
    def run(self):
        """Запускает полный экспорт"""
        print("="*60)
        print("🤖 ЭКСПОРТ СТРУКТУРЫ МЕНЮ БОТА")
        print("="*60)
        print(f"📁 Файл бота: {self.bot_file}")
        print(f"📁 Целевой каталог: {self.output_dir}")
        print("-"*60)
        
        if not self.parse_file():
            return
        
        # Экспорты
        self.export_structure()
        self.export_menu_tree()
        self.export_markdown()
        
        print("\n" + "="*60)
        print("✅ ГОТОВО!")
        print(f"📄 Результаты в: {self.output_dir}")
        print("="*60)


def main():
    # Путь к файлу бота
    bot_file = local_config.osbb_root / "Bots" / "parking_bot.py"
    
    # Выходной каталог
    output_dir = local_config.output_dir / "04_bot_docs"
    
    exporter = BotMenuExporter(bot_file, output_dir)
    exporter.run()


if __name__ == "__main__":
    main()