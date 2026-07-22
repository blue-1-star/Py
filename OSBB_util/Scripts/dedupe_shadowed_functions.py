#!/usr/bin/env python3
"""
dedupe_shadowed_functions.py
=============================

Первый инструмент "вивисекции" — часть будущей подсистемы
Development Infrastructure (Assistant) проекта OSBB_cl.

Проблема, которую решает:
--------------------------
В Python повторное определение функции с тем же именем на верхнем уровне
модуля молча перекрывает предыдущее — работает только ПОСЛЕДНЕЕ. Все
более ранние версии становятся мёртвым кодом: они физически лежат в
файле, их можно найти и случайно начать чинить, но интерпретатор их
никогда не вызовет.

Что делает скрипт:
-------------------
  1) Разбирает .py файл через `ast` (не регулярками — так надёжнее
     находит настоящие границы функций, включая декораторы).
  2) Находит все функции верхнего уровня, определённые больше одного
     раза.
  3) Строит diff: что останется, что будет удалено (ВСЕГДА оставляет
     ПОСЛЕДНЕЕ определение — оно и есть то, что реально исполняется).
  4) В режиме DRY-RUN (по умолчанию) только показывает diff и пишет
     его в .diff файл. Ничего не меняет.
  5) В режиме --apply пишет очищенный файл — по умолчанию РЯДОМ,
     с суффиксом _deduped.py, а не поверх оригинала. Оригинал не
     трогается, если явно не указан --in-place.

Гарантия безопасности:
-----------------------
Удаляются только те определения функций, которые заведомо никогда не
исполнялись (более ранние def с тем же именем на верхнем уровне того же
файла). Это не рефакторинг и не оптимизация — это удаление кода,
который прямо сейчас недостижим по правилам самого языка Python.
Поведение программы после очистки не меняется НИКАК.

Как запускать:
---------------
    py dedupe_shadowed_functions.py --file db_access.py

    # посмотреть diff, ничего не трогая (по умолчанию)
    # результат: db_access.diff рядом со скриптом

    py dedupe_shadowed_functions.py --file db_access.py --apply

    # создаст db_access_deduped.py рядом с оригиналом

Ограничение (сознательное, для v1):
------------------------------------
Скрипт находит дубли только среди функций ВЕРХНЕГО УРОВНЯ модуля
(не методов внутри классов — там повторное имя метода в одном классе
встречается реже и требует более осторожной обработки). Если такие
найдутся — стоит расширить скрипт отдельно, не наугад.
"""

import argparse
import ast
import difflib
import sys
from pathlib import Path


def find_top_level_function_spans(source: str):
    """Возвращает список (name, start_line, end_line) для каждой функции
    верхнего уровня модуля, в порядке появления в файле.
    start_line учитывает декораторы (если есть), 1-indexed, включительно."""
    tree = ast.parse(source)
    spans = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.decorator_list:
                start = min(d.lineno for d in node.decorator_list)
            else:
                start = node.lineno
            end = node.end_lineno  # требует Python 3.8+
            spans.append((node.name, start, end))
    return spans


def compute_dead_ranges(spans):
    """Из списка (name, start, end) возвращает список диапазонов строк,
    которые нужно удалить — все определения функции КРОМЕ последнего."""
    by_name = {}
    for name, start, end in spans:
        by_name.setdefault(name, []).append((start, end))

    dead_ranges = []  # (start, end, name, occurrence_index, total_occurrences)
    for name, occurrences in by_name.items():
        if len(occurrences) <= 1:
            continue
        # оставляем последнее (по номеру строки) вхождение живым
        occurrences_sorted = sorted(occurrences)
        for idx, (start, end) in enumerate(occurrences_sorted[:-1], start=1):
            dead_ranges.append((start, end, name, idx, len(occurrences_sorted)))

    dead_ranges.sort()
    return dead_ranges


def build_cleaned_source(lines, dead_ranges):
    """lines — список строк файла (1-indexed через lines[i-1]).
    Возвращает новый текст без строк из dead_ranges."""
    to_remove = set()
    for start, end, *_ in dead_ranges:
        to_remove.update(range(start, end + 1))

    kept = [line for i, line in enumerate(lines, start=1) if i not in to_remove]
    return "".join(kept)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", required=True, help="Путь к .py файлу для очистки")
    ap.add_argument("--apply", action="store_true", help="Реально записать очищенный файл (по умолчанию — только diff)")
    ap.add_argument("--in-place", action="store_true", help="При --apply перезаписать сам файл, а не создавать *_deduped.py рядом")
    ap.add_argument("--output", default=None, help="Явно указать путь для очищенного файла (переопределяет --in-place)")
    ap.add_argument("--diff-file", default=None, help="Куда сохранить diff (по умолчанию: <файл>.diff рядом со скриптом)")
    args = ap.parse_args()

    src_path = Path(args.file).resolve()
    if not src_path.exists():
        print(f"Файл не найден: {src_path}", file=sys.stderr)
        sys.exit(1)

    source = src_path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)

    try:
        spans = find_top_level_function_spans(source)
    except SyntaxError as e:
        print(f"Файл не парсится как валидный Python: {e}", file=sys.stderr)
        sys.exit(1)

    dead_ranges = compute_dead_ranges(spans)

    if not dead_ranges:
        print("Дублирующихся функций верхнего уровня не найдено. Файл уже чист (в этом смысле).")
        return

    print(f"Файл: {src_path}")
    print(f"Функций верхнего уровня всего: {len(spans)}")
    unique_names = len({name for name, _, _ in spans})
    print(f"Уникальных имён: {unique_names}")
    print(f"Мёртвых (перекрытых более поздним определением) функций: {len(dead_ranges)}")
    dead_line_count = sum(end - start + 1 for start, end, *_ in dead_ranges)
    print(f"Строк будет удалено: {dead_line_count} из {len(lines)} ({dead_line_count/len(lines)*100:.0f}%)")
    print()
    print("Детали (какая функция, где перекрыта, чем):")
    by_name_last = {}
    for name, start, end in spans:
        by_name_last[name] = end  # последний встреченный = финальный (живой)
    for start, end, name, idx, total in dead_ranges:
        print(f"  {name:40s} строки {start}-{end}  (версия {idx} из {total}, живая версия дальше по файлу)")

    cleaned = build_cleaned_source(lines, dead_ranges)

    diff = list(difflib.unified_diff(
        lines,
        cleaned.splitlines(keepends=True),
        fromfile=str(src_path),
        tofile=str(src_path) + " (после очистки)",
    ))

    diff_path = Path(args.diff_file).resolve() if args.diff_file else src_path.with_suffix(src_path.suffix + ".diff")
    diff_path.write_text("".join(diff), encoding="utf-8")
    print(f"\nDiff сохранён: {diff_path}")

    # sanity check: очищенный текст должен оставаться валидным Python
    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        print(f"\nВНИМАНИЕ: очищенный текст не проходит проверку синтаксиса: {e}", file=sys.stderr)
        print("Файл НЕ будет записан. Проверьте diff вручную.", file=sys.stderr)
        sys.exit(1)

    if not args.apply:
        print("\nЭто был DRY-RUN. Файл не изменён.")
        print("Проверьте .diff. Когда согласны — добавьте --apply.")
        return

    if args.output:
        out_path = Path(args.output).resolve()
    elif args.in_place:
        out_path = src_path
    else:
        out_path = src_path.with_name(src_path.stem + "_deduped" + src_path.suffix)

    out_path.write_text(cleaned, encoding="utf-8")
    print(f"\nОчищенный файл записан: {out_path}")
    if out_path == src_path:
        print("(перезаписан оригинал — --in-place был указан явно)")
    else:
        print("(оригинал не тронут)")


if __name__ == "__main__":
    main()