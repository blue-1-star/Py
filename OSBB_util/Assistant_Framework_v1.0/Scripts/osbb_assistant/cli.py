from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import VERSION
from .common import find_project_root
from .exporters.resolver import run as run_resolver_export
from .legacy_commands import cmd_check, cmd_compare, cmd_doctor, cmd_hash, cmd_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="assistant",
        description=f"OSBB Utility Assistant v{VERSION}",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("check", help="Проверить структуру проекта.")
    sub.add_parser("doctor", help="Выполнить подробную диагностику.")
    sub.add_parser("report", help="Сформировать единый отчёт для рабочего чата.")

    hash_parser = sub.add_parser("hash", help="Показать SHA256 контролируемых файлов.")
    hash_parser.add_argument("file", nargs="?", help="Имя файла; без имени — все.")

    compare_parser = sub.add_parser("compare", help="Сравнить локальный файл с Git HEAD.")
    compare_parser.add_argument("file", nargs="?", help="Имя файла; без имени — все.")

    export_parser = sub.add_parser("export", help="Экспортировать данные проекта.")
    export_sub = export_parser.add_subparsers(dest="export_command")
    resolver = export_sub.add_parser("resolver", help="Создать отчёт для разработки Resolver Layer.")
    resolver.add_argument("--db", help="Явный путь к SQLite-базе; иначе база ищется автоматически.")
    resolver.add_argument("--output", help="Каталог для отчёта; по умолчанию OSBB_util/Exports.")
    resolver.add_argument("--full", action="store_true", help="Включить все таблицы, а не только Resolver-кандидаты.")
    resolver.add_argument("--samples", type=int, default=5, help="Число строк-образцов на таблицу (по умолчанию 5).")
    resolver.add_argument("--no-data", action="store_true", help="Не включать образцы данных.")
    resolver.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Не скрывать потенциально чувствительные поля в образцах.",
    )

    sub.add_parser("help", help="Показать справку.")
    return parser


def main(script_path: Path, argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in {None, "help"}:
        parser.print_help()
        return 0
    if args.command == "export" and not args.export_command:
        parser.parse_args(["export", "--help"])
        return 0
    if getattr(args, "samples", 1) < 0:
        parser.error("--samples не может быть отрицательным")

    try:
        root = find_project_root(Path.cwd())
        commands = {
            "check": cmd_check,
            "doctor": cmd_doctor,
            "report": cmd_report,
            "hash": cmd_hash,
            "compare": cmd_compare,
        }
        if args.command in commands:
            return commands[args.command](root, args)
        if args.command == "export" and args.export_command == "resolver":
            return run_resolver_export(root, args, script_path)
        parser.error("Неизвестная команда")
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print(f"Assistant ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nОперация прервана пользователем.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Assistant ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
