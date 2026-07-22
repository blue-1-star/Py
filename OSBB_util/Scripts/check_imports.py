#!/usr/bin/env python3
"""
check_imports.py
===================

Статический аудит импортов по всему OSBB_cl — без реального выполнения
файлов (безопасно: не подключается к Telegram/БД, не запускает никакой
код, только разбирает исходники через `ast`).

Что делает:
  1) Строит карту всех .py файлов/пакетов, которые реально существуют
     в OSBB_cl — это "известные" локальные модули.
  2) Для каждого .py файла разбирает все `import X` / `from X import Y`
     верхнего уровня (и относительные `from . import x` / `from ..a import b`).
  3) Каждое имя из первого сегмента (`Bots`, `handlers`, `core_new`,
     `config`, и т.п.) сверяет с картой локальных модулей и со списком
     известных стандартных/сторонних библиотек.
  4) Всё, что не нашлось ни там, ни там — помечается как "требует проверки"
     (это не обязательно ошибка — может быть сторонний pip-пакет,
     которого просто нет в списке ниже, но чаще всего это как раз
     сломанный после переноса путь).

Отчёт группируется по имени модуля, а не по файлу — так сразу видно,
что "Bots" не резолвится в 40 файлах, а не читать 40 похожих строк.

Как запускать:

    python check_imports.py --root "G:\\Programming\\OSBB_cl"

Результат — в консоль и в import_audit_report.csv рядом со скриптом.
Это read-only диагностика, флага --apply нет и не нужен.
"""

import argparse
import ast
import csv
import sys
from pathlib import Path

# Стандартная библиотека + типичные сторонние пакеты проекта — не флагуем.
KNOWN_EXTERNAL = {
    "sys", "os", "re", "json", "csv", "sqlite3", "shutil", "argparse",
    "pathlib", "datetime", "typing", "dataclasses", "functools", "itertools",
    "collections", "logging", "traceback", "time", "math", "random",
    "subprocess", "io", "abc", "enum", "contextlib", "asyncio", "platform",
    "unittest", "difflib", "ast", "importlib", "copy", "hashlib", "uuid",
    "telegram", "requests", "openpyxl", "pandas", "numpy", "docx",
    "PyPDF2", "PIL", "dotenv", "pytz", "sqlalchemy", "aiohttp",
    "__future__",
    # добавлено после первого реального прогона:
    "warnings", "glob", "types", "zipfile", "xml", "decimal", "inspect",
    "calendar", "py_compile", "telethon", "dateutil", "pickle", "base64",
    "textwrap", "string", "queue", "threading", "socket", "struct",
}

SKIP_DIR_NAMES = {"__pycache__", ".git", "_unsorted"}


def build_local_module_map(root: Path) -> set:
    """Возвращает множество допустимых dotted-имён для всех .py файлов
    под root — не только полный путь от корня, но и КАЖДЫЙ суффикс пути.

    Суффиксы нужны из-за паттерна в этом проекте: файлы сами добавляют
    свою папку в sys.path (см. client_portal_v3.py — вставляет BOTS_DIR
    в sys.path), из-за чего `handlers.X` резолвится, даже если `handlers/`
    физически лежит внутри `Bots/`, а не в корне. Статически предсказать
    каждую такую вставку невозможно, поэтому разрешаем совпадение по
    любому суффиксу пути — это соответствует тому, как реально ведёт себя
    этот код, и совпадает с фактическим поведением, а не только "чистым"
    случаем импорта от корня проекта.
    """
    known = set()
    for p in root.rglob("*.py"):
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        rel = p.relative_to(root).with_suffix("")
        parts = rel.parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if not parts:
            continue
        # полный путь и все префиксы от корня (как раньше)
        for i in range(1, len(parts) + 1):
            known.add(".".join(parts[:i]))
        # плюс все суффиксы (новое) — учитывает сценарий "своя папка в sys.path"
        for i in range(len(parts)):
            known.add(".".join(parts[i:]))

    # Голые пакеты-директории (namespace packages, Python 3 не требует
    # __init__.py вообще) — например, "handlers" импортируется целиком
    # (`from handlers import client_portal as base`), без вложенного имени.
    for d in root.rglob("*"):
        if not d.is_dir():
            continue
        if any(part in SKIP_DIR_NAMES for part in d.parts):
            continue
        parts = d.relative_to(root).parts
        if not parts:
            continue
        for i in range(1, len(parts) + 1):
            known.add(".".join(parts[:i]))
        for i in range(len(parts)):
            known.add(".".join(parts[i:]))

    return known


def extract_top_level_imports(source: str, file_rel: str):
    """Возвращает список (module_name, level) — верхнеуровневые
    импортированные имена в файле. level=0 значит абсолютный импорт,
    level>=1 — относительный (количество точек)."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return None, str(e)

    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append((alias.name, 0))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                names.append((node.module or "", node.level))
            elif node.module:
                names.append((node.module, 0))
    return names, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help=r'Корень OSBB_cl, например "G:\Programming\OSBB_cl"')
    ap.add_argument("--report", default="import_audit_report.csv", help="Имя CSV-отчёта")
    ap.add_argument("--include-unsorted", action="store_true", help="Проверять и файлы внутри _unsorted/ (по умолчанию пропускаются)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Папка не найдена: {root}", file=sys.stderr)
        sys.exit(1)

    skip_dirs = set(SKIP_DIR_NAMES)
    if args.include_unsorted:
        skip_dirs.discard("_unsorted")

    known_local = build_local_module_map(root)

    py_files = [
        p for p in root.rglob("*.py")
        if not any(part in skip_dirs for part in p.parts)
    ]

    problems = []  # (file_rel, missing_module, first_segment)
    syntax_errors = []

    for p in py_files:
        rel = str(p.relative_to(root))
        try:
            source = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            syntax_errors.append((rel, f"read error: {e}"))
            continue

        names, err = extract_top_level_imports(source, rel)
        if err:
            syntax_errors.append((rel, err))
            continue

        for module_name, level in names:
            if level > 0:
                # относительный импорт: level=1 -> текущий пакет (папка файла),
                # level=2 -> на 1 выше, и т.д. Считаем от папки файла.
                file_dir_parts = p.relative_to(root).parent.parts
                cut = level - 1
                base_parts = file_dir_parts[: len(file_dir_parts) - cut] if cut < len(file_dir_parts) else ()
                module_parts = tuple(module_name.split(".")) if module_name else ()
                candidate = ".".join(base_parts + module_parts)
                if candidate not in known_local and module_name not in known_local:
                    problems.append((rel, module_name, "(relative) " + module_name))
                continue

            first_segment = module_name.split(".")[0]
            if first_segment in KNOWN_EXTERNAL:
                continue
            if first_segment in known_local or module_name in known_local:
                continue

            problems.append((rel, module_name, first_segment))

    print(f"Проверено файлов: {len(py_files)}")
    print(f"С синтаксическими/читательскими ошибками: {len(syntax_errors)}")
    for rel, err in syntax_errors:
        print(f"  {rel}: {err}")
    print(f"Неразрешённых импортов (записей): {len(problems)}")

    by_module = {}
    for rel, module_name, first_segment in problems:
        by_module.setdefault(first_segment, []).append((rel, module_name))

    print("\n=== СВОДКА ПО МОДУЛЯМ (что чаще всего не резолвится) ===")
    for mod, entries in sorted(by_module.items(), key=lambda x: -len(x[1])):
        print(f"  {mod:35s} затронуто файлов: {len(entries)}")

    report_path = Path(args.report).resolve()
    with report_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "unresolved_module", "first_segment"])
        for rel, module_name, first_segment in problems:
            writer.writerow([rel, module_name, first_segment])
        for rel, err in syntax_errors:
            writer.writerow([rel, "SYNTAX_ERROR", err])

    print(f"\nПодробный отчёт: {report_path}")
    print("\nНапоминание: это статическая проверка. 'Неразрешённый' модуль может")
    print("оказаться сторонним pip-пакетом, которого просто нет в списке KNOWN_EXTERNAL —")
    print("не обязательно ошибка переноса, но каждый стоит просмотреть.")


if __name__ == "__main__":
    main()