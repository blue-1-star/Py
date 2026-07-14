#!/usr/bin/env python
"""
Анализ мертвого кода в проекте OSBB
Находит:
- Неиспользуемые функции
- Неиспользуемые импорты
- Функции, которые определены, но не вызываются
"""

import ast
import sys
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List, Tuple
from datetime import datetime  # ⬅️ ДОБАВЛЕНО
# Подавляем предупреждения о нестандартных escape-последовательностях
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)


# Добавляем пути
UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

from local_config import local_config


class CodeAnalyzer:
    """Анализирует код на наличие мертвых функций и импортов"""
    
    def __init__(self, root_path: Path):
        self.root = root_path
        self.functions: Dict[str, Set[str]] = defaultdict(set)  # файл -> {функции}
        self.calls: Dict[str, Set[str]] = defaultdict(set)      # файл -> {вызовы}
        self.imports: Dict[str, Set[str]] = defaultdict(set)    # файл -> {импорты}
        self.defined_in_file: Dict[str, str] = {}               # функция -> файл
        
        # Исключаем стандартные библиотеки и внешние
        self.skip_modules = {
            'telegram', 'sqlite3', 'datetime', 'pathlib', 'sys',
            'typing', 're', 'json', 'subprocess', 'os', 'math',
            'random', 'time', 'logging', 'collections', 'itertools',
            'functools', 'enum', 'dataclasses', 'config', 'local_config',
        }
    
    def analyze_file(self, filepath: Path) -> None:
        """Анализирует один Python файл"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return
        
        # Собираем определенные функции
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                # Игнорируем встроенные и специальные
                if func_name.startswith('_') and func_name not in ['__init__', '__call__']:
                    continue
                self.functions[str(filepath)].add(func_name)
                self.defined_in_file[func_name] = str(filepath)
            
            # Собираем вызовы функций
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    call_name = node.func.id
                    # Игнорируем встроенные функции Python
                    if call_name not in dir(__builtins__):
                        self.calls[str(filepath)].add(call_name)
                elif isinstance(node.func, ast.Attribute):
                    # Проверяем, не является ли это импортированной функцией
                    if isinstance(node.func.value, ast.Name):
                        # Это вызов типа module.function()
                        pass
        
        # Собираем импорты
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split('.')[0]
                    if module not in self.skip_modules:
                        self.imports[str(filepath)].add(module)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] not in self.skip_modules:
                    self.imports[str(filepath)].add(node.module.split('.')[0])
    
    def analyze_project(self) -> None:
        """Анализирует весь проект"""
        print("🔍 Анализ кода...")
        py_files = list(self.root.rglob("*.py"))
        
        # Исключаем venv и __pycache__
        py_files = [f for f in py_files if 'venv' not in str(f) and '__pycache__' not in str(f)]
        
        print(f"📁 Найдено Python файлов: {len(py_files)}")
        
        for filepath in py_files:
            self.analyze_file(filepath)
        
        print(f"📊 Найдено функций: {len(self.defined_in_file)}")
        print(f"📊 Найдено вызовов: {sum(len(c) for c in self.calls.values())}")
    
    def find_dead_functions(self) -> List[Tuple[str, str]]:
        """Находит функции, которые не вызываются"""
        dead = []
        
        all_calls = set()
        for calls in self.calls.values():
            all_calls.update(calls)
        
        for func_name, filepath in self.defined_in_file.items():
            # Игнорируем обработчики, которые могут вызываться через регистрацию
            if func_name.startswith('handle_'):
                continue
            if func_name.startswith('show_'):
                continue
            if func_name in ['main', 'run', 'start']:
                continue
            
            if func_name not in all_calls:
                dead.append((func_name, filepath))
        
        return sorted(dead, key=lambda x: x[1])
    
    def find_unused_imports(self) -> Dict[str, Set[str]]:
        """Находит неиспользуемые импорты"""
        unused = {}
        
        for filepath, imports in self.imports.items():
            # Проверяем, используется ли импорт в файле
            used_in_file = set()
            for call in self.calls.get(filepath, set()):
                # Проверяем, является ли вызов импортированным
                for imp in imports:
                    if call.startswith(imp) or call == imp:
                        used_in_file.add(imp)
            
            unused_imports = imports - used_in_file
            if unused_imports:
                unused[filepath] = unused_imports
        
        return unused
    
    def generate_report(self) -> str:
        """Генерирует отчет"""
        lines = []
        lines.append("=" * 70)
        lines.append("📊 ОТЧЕТ ПО МЕРТВОМУ КОДУ")
        lines.append("=" * 70)
        lines.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        
        # 1. Мертвые функции
        dead = self.find_dead_functions()
        lines.append(f"🔴 НЕИСПОЛЬЗУЕМЫЕ ФУНКЦИИ: {len(dead)}")
        lines.append("-" * 70)
        
        if dead:
            for func_name, filepath in dead[:50]:
                # Сокращаем путь
                short_path = filepath.replace(str(self.root), '...')
                lines.append(f"  • {func_name}() → {short_path}")
            if len(dead) > 50:
                lines.append(f"  ... и еще {len(dead) - 50} функций")
        else:
            lines.append("  ✅ Мертвых функций не найдено")
        
        lines.append("")
        
        # 2. Неиспользуемые импорты
        unused_imports = self.find_unused_imports()
        lines.append(f"🟡 НЕИСПОЛЬЗУЕМЫЕ ИМПОРТЫ: {sum(len(v) for v in unused_imports.values())}")
        lines.append("-" * 70)
        
        if unused_imports:
            for filepath, imports in list(unused_imports.items())[:20]:
                short_path = filepath.replace(str(self.root), '...')
                lines.append(f"  📄 {short_path}")
                for imp in imports:
                    lines.append(f"    • {imp}")
            if len(unused_imports) > 20:
                lines.append(f"  ... и еще {len(unused_imports) - 20} файлов")
        else:
            lines.append("  ✅ Неиспользуемых импортов не найдено")
        
        lines.append("")
        
        # 3. Статистика
        lines.append("📊 СТАТИСТИКА")
        lines.append("-" * 70)
        lines.append(f"  Всего файлов проанализировано: {len(self.functions)}")
        lines.append(f"  Всего функций определено: {len(self.defined_in_file)}")
        lines.append(f"  Всего уникальных вызовов: {sum(len(c) for c in self.calls.values())}")
        lines.append(f"  Всего импортов: {sum(len(i) for i in self.imports.values())}")
        
        return "\n".join(lines)


def main():
    print("=" * 70)
    print("🔍 АНАЛИЗ МЕРТВОГО КОДА")
    print("=" * 70)
    
    # Анализируем только OSBB/
    root = local_config.osbb_root
    print(f"📁 Анализируем: {root}")
    
    analyzer = CodeAnalyzer(root)
    analyzer.analyze_project()
    
    # Генерируем отчет
    report = analyzer.generate_report()
    
    # Сохраняем в файл
    output_dir = local_config.output_dir / "03_code_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / "dead_code_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "=" * 70)
    print(f"✅ Отчет сохранен: {report_file}")
    print("=" * 70)
    
    # Показываем краткий итог
    print("\n📋 КРАТКИЙ ИТОГ:")
    lines = report.split('\n')
    for line in lines[:30]:
        print(line)


if __name__ == "__main__":
    main()