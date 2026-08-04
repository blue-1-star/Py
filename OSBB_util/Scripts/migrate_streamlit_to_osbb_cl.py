#!/usr/bin/env python3
"""
migrate_streamlit_to_osbb_cl.py
==================================

Перенос (КОПИРОВАНИЕ, не перемещение) дерева Streamlit-инструментов
из OSBB_util в OSBB_cl.

Контекст решения (см. Project_Log.md за сегодня): пока Streamlit был
read-only просмотрщиком (03_payments_viewer.py), раздельное
расположение было оправдано — обслуживающая утилита сбоку, ничего не
пишет, дублировать нечего. С появлением редактора (04_cashbox_editor.py),
который пишет в payments/cashbox_operations/cashier_receipts и
пересчитывает cashboxes.current_balance, граница "проект / утилита"
обязана совпасть с границей "чтение / запись" — иначе бизнес-правила
(формула баланса, структура audit_log) неизбежно дублируются в двух
местах и расходятся, ровно как уже случилось однажды с
apply_cleanup_batch(), не пересчитывавшим баланс (см. Surgical_Delete.md).

Верхняя папка переименовывается: streamlit_apps -> admin_console
(это уже не "утилита сбоку", а вторая презентационная поверхность над
тем же Finance Core, что и бот). Внутренняя структура (pages/, utils/,
home.py) НЕ меняется и не переименовывается — по тому же принципу
"ноль поломок импортов", что и в migrate_to_osbb_cl.py: страницы уже
вычисляют свой корень относительно __file__
(STREAMLIT_ROOT = Path(__file__).resolve().parent.parent), поэтому
переезд верхней папки сам по себе импорты не ломает.

Что скрипт НЕ делает:
- не трогает исходную папку в OSBB_util (копирование, не move);
- не переписывает импорты внутри файлов;
- не проверяет, что get_conn() в utils/db.py указывает на правильную
  базу после переезда — см. блок "ТРЕБУЕТ РУЧНОЙ ПРОВЕРКИ" в отчёте.

Расположение (рядом с migrate_to_osbb_cl.py — тот же класс объекта,
одноразовый bootstrap-скрипт, физически на стороне источника):

    G:\Programming\Py\OSBB_util\Scripts\migrate_streamlit_to_osbb_cl.py

Как запускать (из папки Scripts):

    cd "G:\Programming\Py\OSBB_util\Scripts"
    python migrate_streamlit_to_osbb_cl.py ^
        --source "G:\\Programming\\Py\\OSBB_util\\streamlit_apps" ^
        --dest   "G:\\Programming\\OSBB_cl\\admin_console"

Сначала DRY RUN (по умолчанию) — только отчёт. Добавьте --apply, когда
согласны, чтобы реально скопировать.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

SKIP_NAMES = {"__pycache__", ".git", ".venv", "venv"}
SKIP_SUFFIXES = {".pyc"}

# Пути (относительно source), которые НЕ переносим — например, если там
# случайно лежит локальная копия .db или .env с секретами.
EXPLICIT_SKIP = set()

# По этим паттернам ищем зашитые старые пути после копирования —
# чтобы не пропустить хардкод вроде "OSBB_util" в db.py/config.
SUSPECT_PATTERNS = [
    re.compile(r"OSBB_util", re.IGNORECASE),
    re.compile(r"streamlit_apps", re.IGNORECASE),
    re.compile(r"G:\\Programming\\Py", re.IGNORECASE),
]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".cfg", ".ini", ".toml"}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_NAMES for part in path.parts):
        return True
    if path.suffix in SKIP_SUFFIXES:
        return True
    return False


def scan_for_hardcoded_paths(dest: Path) -> list[tuple[str, str, str]]:
    """Ищет в скопированных текстовых файлах ссылки на старое расположение."""
    findings = []
    for p in dest.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_SUFFIXES:
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern in SUSPECT_PATTERNS:
            m = pattern.search(content)
            if m:
                rel = str(p.relative_to(dest)).replace("\\", "/")
                findings.append((rel, pattern.pattern, m.group(0)))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help=r'Корень streamlit_apps в OSBB_util, например "G:\Programming\Py\OSBB_util\streamlit_apps"')
    ap.add_argument("--dest", required=True, help=r'Новое расположение в OSBB_cl, например "G:\Programming\OSBB_cl\admin_console"')
    ap.add_argument("--skip", action="append", default=[], help='Доп. относительный путь для пропуска (можно указать несколько раз)')
    ap.add_argument("--apply", action="store_true", help="Реально скопировать (по умолчанию — только отчёт)")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()

    if not source.exists():
        print(f"Источник не найден: {source}", file=sys.stderr)
        sys.exit(1)
    if dest.exists() and any(dest.iterdir()):
        print(f"Назначение уже существует и не пусто: {dest}", file=sys.stderr)
        print("Проверьте вручную, не перезаписываем автоматически.", file=sys.stderr)
        sys.exit(1)

    explicit_skip = EXPLICIT_SKIP | {s.replace("\\", "/") for s in args.skip}

    all_files = [p for p in source.rglob("*") if p.is_file() and not should_skip(p)]

    plan = []
    skipped = []
    for p in all_files:
        rel = str(p.relative_to(source)).replace("\\", "/")
        if rel in explicit_skip:
            skipped.append(rel)
            continue
        plan.append((p, rel))

    print(f"Источник: {source}")
    print(f"Назначение: {dest}")
    print(f"Режим: копирование верхней папки с переименованием (streamlit_apps -> admin_console),")
    print(f"       внутренняя структура (pages/, utils/, home.py) не меняется")
    print(f"Всего файлов найдено: {len(all_files)}")
    print(f"К переносу: {len(plan)}")
    if skipped:
        print(f"Явно пропущено: {len(skipped)}")
        for s in skipped:
            print(f"  пропуск: {s}")
    print()
    print("Файлы к переносу:")
    for _, rel in sorted(plan, key=lambda x: x[1]):
        print(f"  {rel}")

    if not args.apply:
        print("\nЭто был DRY RUN. Ничего не скопировано.")
        print("Проверьте список выше. Когда согласны — запустите с --apply.")
        return

    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src_path, rel in plan:
        dst_path = dest / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        copied += 1

    print(f"\nСкопировано файлов: {copied}")
    print("Исходная папка в OSBB_util не тронута — это было копирование, не перемещение.")

    print("\n--- Проверка на зашитые старые пути ---")
    findings = scan_for_hardcoded_paths(dest)
    if not findings:
        print("Не найдено упоминаний OSBB_util / streamlit_apps / старого пути в скопированных файлах.")
    else:
        print(f"ТРЕБУЕТ РУЧНОЙ ПРОВЕРКИ — найдено {len(findings)} подозрительных мест:")
        for rel, pattern, matched in findings:
            print(f"  {rel}: совпадение по «{pattern}» -> «{matched}»")
        print("\nЭто не обязательно ошибка (может быть просто упоминание в комментарии/докстринге),")
        print("но каждое место стоит открыть и убедиться, что путь к БД и импорты")
        print("после переезда по-прежнему корректны.")

    print(f"\nГотово. Дальше: обновить sys.path.insert в home.py, если он ссылается")
    print(f"на старое расположение напрямую (а не через Path(__file__).resolve()),")
    print(f"и один раз руками открыть {dest / 'home.py'} в Streamlit, чтобы проверить, что всё поднимается.")


if __name__ == "__main__":
    main()