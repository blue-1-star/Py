#!/usr/bin/env python3
"""
migrate_to_osbb_cl.py
========================

Массовый перенос (КОПИРОВАНИЕ, не перемещение) всего, что реально
осталось в OSBB после чистки триаж-скриптом, в OSBB_cl — ЗЕРКАЛЬНО,
теми же именами и структурой папок, что и в старом OSBB.

Почему зеркально, а не по подсистемам: любое переименование папок ломает
внутренние импорты (`from Bots.db_access import ...`, `from access_control
import ...` и т.п.) — а значит, каждый файл пришлось бы чинить руками
до того, как что-либо вообще заработает. Зеркальная копия — ноль поломок
импортов. Реорганизация по смысловым подсистемам (presentation/,
business_core/ и т.п.) — отдельная, постепенная задача на будущее, по
аналогии с тем, как в своё время core_new внедрялся через мягкую
прослойку-адаптер (db_adapter.py), а не одним рывком.

Старый OSBB не трогается — он остаётся как был, работает на своём месте.
Файловая система уже физически разделена триаж-скриптом: то, что ушло
в архив (--apply), больше не лежит в OSBB\\ — git-ветки тут ни при чём,
это обычное состояние диска.

Пропускается всегда: __pycache__, .git, .pyc, и явно указанные пути
(например core_new/db_access.py, если он уже вручную положен на своё
место в другой локации).

Как запускать:

    python migrate_to_osbb_cl.py --source "G:\\Programming\\Py\\OSBB" --dest "G:\\Programming\\OSBB_cl"

Сначала DRY RUN (по умолчанию) — только отчёт, что куда ляжет.
Добавьте --apply, когда согласны, чтобы реально скопировать.
"""

import argparse
import shutil
import sys
from pathlib import Path

SKIP_NAMES = {"__pycache__", ".git"}
SKIP_SUFFIXES = {".pyc"}

# Пути (относительно source), которые НЕ переносим — уже размещены вручную
# в другом месте, не затираем.
EXPLICIT_SKIP = set()


def should_skip(path: Path) -> bool:
    if any(part in SKIP_NAMES for part in path.parts):
        return True
    if path.suffix in SKIP_SUFFIXES:
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help=r'Корень очищенного OSBB, например "G:\Programming\Py\OSBB"')
    ap.add_argument("--dest", required=True, help=r'Корень OSBB_cl, например "G:\Programming\OSBB_cl"')
    ap.add_argument("--skip", action="append", default=[], help=r'Доп. относительный путь для пропуска (можно указать несколько раз), например --skip "core_new/db_access.py"')
    ap.add_argument("--apply", action="store_true", help="Реально скопировать (по умолчанию — только отчёт)")
    args = ap.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()

    if not source.exists():
        print(f"Источник не найден: {source}", file=sys.stderr)
        sys.exit(1)
    if not dest.exists():
        print(f"Назначение не найдено: {dest} — сначала запустите init_osbb_cl_skeleton.py", file=sys.stderr)
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

    top_level_counts = {}
    for _, rel in plan:
        bucket = rel.split("/")[0]
        top_level_counts[bucket] = top_level_counts.get(bucket, 0) + 1

    print(f"Источник: {source}")
    print(f"Назначение: {dest}")
    print(f"Режим: ЗЕРКАЛЬНОЕ копирование (структура папок не меняется)")
    print(f"Всего файлов найдено: {len(all_files)}")
    print(f"К переносу: {len(plan)}")
    print(f"Явно пропущено: {len(skipped)}")
    for s in skipped:
        print(f"  пропуск: {s}")
    print()
    print("По папкам верхнего уровня (для ориентира, без переименований):")
    for bucket, count in sorted(top_level_counts.items(), key=lambda x: -x[1]):
        print(f"  {bucket:25s} {count:4d} файлов")

    if not args.apply:
        print("\nЭто был DRY RUN. Ничего не скопировано.")
        print("Проверьте план выше. Когда согласны — запустите с --apply.")
        return

    copied = 0
    for src_path, rel in plan:
        dst_path = dest / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        copied += 1

    print(f"\nСкопировано файлов: {copied}")
    print("Готово. Исходный OSBB не тронут — это было копирование, не перемещение.")


if __name__ == "__main__":
    main()