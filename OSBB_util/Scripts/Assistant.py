#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assistant.py
OSBB Utility Assistant v0.3

Безопасная диагностическая версия.
По умолчанию ничего не изменяет в проекте.

Команды:
    python Assistant.py check
    python Assistant.py doctor
    python Assistant.py report
    python Assistant.py hash [имя_файла]
    python Assistant.py compare [имя_файла]
    python Assistant.py help
"""

from __future__ import annotations

import argparse
import hashlib
import platform
import subprocess
import sys
from pathlib import Path

VERSION = "0.3"
DEFAULT_ROOT = Path(r"G:\Programming\Py")

TRACKED_FILES = {
    "cashier_v2_ui.py": Path("OSBB/tools/cashier_v2_telegram/cashier_v2_ui.py"),
    "cashier_card.py": Path("OSBB/tools/cashier_v2_telegram/cashier_card.py"),
}


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def find_project_root(start: Path | None = None) -> Path:
    candidates: list[Path] = []

    if start is not None:
        current = start.resolve()
        candidates.extend([current, *current.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])
    candidates.append(DEFAULT_ROOT)

    seen: set[Path] = set()
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)

        if (candidate / ".git").exists() and (candidate / "OSBB").exists():
            return candidate

    raise FileNotFoundError(
        "Не найден корень проекта OSBB.\n"
        f"Ожидался Git-репозиторий с каталогом OSBB, например:\n{DEFAULT_ROOT}"
    )


def file_info(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
        lines = len(text.splitlines())
        encoding = "utf-8"
    except UnicodeDecodeError:
        lines = None
        encoding = "binary/unknown"

    return {
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "lines": lines,
        "encoding": encoding,
    }


def resolve_tracked_file(name: str | None, root: Path) -> list[tuple[str, Path]]:
    if not name:
        return [(key, root / rel) for key, rel in TRACKED_FILES.items()]

    normalized = name.strip().lower()
    matches: list[tuple[str, Path]] = []

    for key, rel in TRACKED_FILES.items():
        if normalized in {key.lower(), rel.name.lower(), str(rel).lower()}:
            matches.append((key, root / rel))

    if not matches:
        available = ", ".join(TRACKED_FILES)
        raise ValueError(f"Неизвестный файл: {name}\nДоступные имена: {available}")
    return matches


def print_header(root: Path) -> None:
    head = run_git(root, "rev-parse", "--short=12", "HEAD")
    commit = head.stdout.strip() if head.returncode == 0 else "UNKNOWN"

    print("=" * 68)
    print(f"OSBB Assistant v{VERSION}")
    print("=" * 68)
    print(f"Project : {root}")
    print(f"Git HEAD : {commit}")
    print()


def status_line(label: str, value: str, ok: bool | None = None) -> None:
    marker = "[ OK ]" if ok is True else "[FAIL]" if ok is False else "      "
    print(f"{marker} {label:<22} {value}")


def cmd_check(root: Path, _args: argparse.Namespace) -> int:
    print_header(root)

    checks = [
        ("Project directory", root),
        ("Git repository", root / ".git"),
        *[(name, root / rel) for name, rel in TRACKED_FILES.items()],
    ]

    failed = False
    for label, path in checks:
        exists = path.exists()
        status_line(label, str(path), exists)
        failed = failed or not exists

    print()
    if failed:
        print("Проверка завершена с ошибками.")
        return 1

    print("Проверка окружения завершена успешно.")
    return 0


def git_worktree_state(root: Path) -> tuple[str, bool]:
    result = run_git(root, "status", "--porcelain")
    if result.returncode != 0:
        return "GIT ERROR", False
    clean = not result.stdout.strip()
    return ("CLEAN" if clean else "MODIFIED"), clean


def cmd_doctor(root: Path, _args: argparse.Namespace) -> int:
    print_header(root)

    state, clean = git_worktree_state(root)
    branch = run_git(root, "branch", "--show-current")
    branch_name = branch.stdout.strip() or "(detached HEAD)"

    status_line("Python", platform.python_version(), True)
    status_line("Platform", platform.platform())
    status_line("Current directory", str(Path.cwd()))
    status_line("Branch", branch_name, branch.returncode == 0)
    status_line("Working tree", state, clean)

    print()
    failed = False
    for name, rel in TRACKED_FILES.items():
        path = root / rel
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            failed = True
            continue

        info = file_info(path)
        line_text = "?" if info["lines"] is None else f'{info["lines"]:,}'
        status_line(name, "OK", True)
        print(f"      Path   : {rel}")
        print(f"      Size   : {info['size_bytes']:,} bytes")
        print(f"      Lines  : {line_text}")
        print(f"      SHA256 : {info['sha256']}")

    print()
    if failed:
        print("Doctor обнаружил проблемы.")
        return 1

    print("Doctor завершил диагностику.")
    return 0


def cmd_report(root: Path, _args: argparse.Namespace) -> int:
    print_header(root)

    branch = run_git(root, "branch", "--show-current")
    branch_name = branch.stdout.strip() or "(detached HEAD)"
    state, clean = git_worktree_state(root)

    status_line("Project", "OK", True)
    status_line("Git repository", "OK", True)
    status_line("Branch", branch_name, branch.returncode == 0)
    status_line("Working tree", state, clean)
    status_line("Python", platform.python_version(), True)
    status_line("Assistant", f"v{VERSION}", True)

    print()
    for name, rel in TRACKED_FILES.items():
        path = root / rel
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            continue
        info = file_info(path)
        print(name)
        print(f"  path    : {rel}")
        print(f"  size    : {info['size_bytes']:,} bytes")
        print(f"  lines   : {info['lines'] if info['lines'] is not None else '?'}")
        print(f"  sha256  : {info['sha256']}")

    print()
    print("Этот отчёт можно целиком копировать в рабочий чат.")
    return 0


def cmd_hash(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    for name, path in resolve_tracked_file(args.file, root):
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            continue
        info = file_info(path)
        print(name)
        print(f"  path    : {path.relative_to(root)}")
        print(f"  sha256  : {info['sha256']}")
        print(f"  size    : {info['size_bytes']:,} bytes")
        print(f"  lines   : {info['lines'] if info['lines'] is not None else '?'}")
        print()

    return 0


def git_blob_hash(root: Path, rel: Path) -> str | None:
    result = run_git(root, "rev-parse", f"HEAD:{rel.as_posix()}")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def local_blob_hash(root: Path, path: Path) -> str | None:
    result = run_git(root, "hash-object", str(path))
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def cmd_compare(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    overall_ok = True
    for name, path in resolve_tracked_file(args.file, root):
        rel = path.relative_to(root)

        if not path.exists():
            status_line(name, "NOT FOUND", False)
            overall_ok = False
            continue

        head_blob = git_blob_hash(root, rel)
        local_blob = local_blob_hash(root, path)

        print(name)
        print(f"  path       : {rel}")
        print(f"  HEAD blob  : {head_blob or 'NOT IN HEAD'}")
        print(f"  Local blob : {local_blob or 'ERROR'}")

        identical = bool(head_blob and local_blob and head_blob == local_blob)
        print(f"  result     : {'IDENTICAL' if identical else 'DIFFERS'}")
        print()

        overall_ok = overall_ok and identical

    return 0 if overall_ok else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="assistant",
        description="OSBB Utility Assistant v0.3 — безопасная диагностика проекта.",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Проверить структуру проекта.")
    sub.add_parser("doctor", help="Выполнить подробную диагностику.")
    sub.add_parser("report", help="Сформировать единый отчёт для рабочего чата.")

    hash_parser = sub.add_parser("hash", help="Показать SHA256 контролируемых файлов.")
    hash_parser.add_argument("file", nargs="?", help="Имя файла; без имени — все.")

    compare_parser = sub.add_parser(
        "compare",
        help="Сравнить локальный файл с его версией в Git HEAD.",
    )
    compare_parser.add_argument("file", nargs="?", help="Имя файла; без имени — все.")

    sub.add_parser("help", help="Показать справку.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in {None, "help"}:
        parser.print_help()
        return 0

    try:
        root = find_project_root(Path.cwd())

        commands = {
            "check": cmd_check,
            "doctor": cmd_doctor,
            "report": cmd_report,
            "hash": cmd_hash,
            "compare": cmd_compare,
        }
        return commands[args.command](root, args)

    except (FileNotFoundError, ValueError) as exc:
        print(f"Assistant ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nОперация прервана пользователем.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Assistant ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
