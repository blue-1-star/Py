#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
Assistant.py
OSBB Utility Assistant v0.4

Единая сервисная точка для диагностики, резервного копирования,
просмотра изменений и безопасного применения patch-файлов.

Расположение:
    G:\Programming\Py\OSBB_util\Scripts\Assistant.py

Команды:
    python Assistant.py check
    python Assistant.py doctor
    python Assistant.py report
    python Assistant.py hash [имя_файла]
    python Assistant.py compare [имя_файла]
    python Assistant.py backup [имя_файла]
    python Assistant.py diff [имя_файла]
    python Assistant.py log [-n 10]
    python Assistant.py apply путь_к_patch
    python Assistant.py apply путь_к_patch --check
    python Assistant.py help
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path

VERSION = "0.4"
DEFAULT_ROOT = Path(r"G:\Programming\Py")
BACKUP_ROOT = Path(r"G:\Programming\Py\OSBB_util\Backups")

TRACKED_FILES = {
    "cashier_v2_ui.py": Path("OSBB/tools/cashier_v2_telegram/cashier_v2_ui.py"),
    "cashier_card.py": Path("OSBB/tools/cashier_v2_telegram/cashier_card.py"),
}


class AssistantError(RuntimeError):
    pass


def run_process(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run_process(["git", "-C", str(root), *args])


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
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)

        if (resolved / ".git").exists() and (resolved / "OSBB").exists():
            return resolved

    raise AssistantError(
        "Не найден корень проекта OSBB.\n"
        "Ожидается Git-репозиторий, содержащий каталог OSBB.\n"
        f"Стандартный путь: {DEFAULT_ROOT}"
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


def resolve_tracked_files(name: str | None, root: Path) -> list[tuple[str, Path]]:
    if not name:
        return [(key, root / rel) for key, rel in TRACKED_FILES.items()]

    normalized = name.strip().lower()
    matches: list[tuple[str, Path]] = []

    for key, rel in TRACKED_FILES.items():
        variants = {
            key.lower(),
            rel.name.lower(),
            rel.as_posix().lower(),
            str(rel).lower(),
        }
        if normalized in variants:
            matches.append((key, root / rel))

    if not matches:
        available = ", ".join(TRACKED_FILES)
        raise AssistantError(
            f"Неизвестный контролируемый файл: {name}\n"
            f"Доступные имена: {available}"
        )

    return matches


def print_header(root: Path) -> None:
    head = run_git(root, "rev-parse", "--short=12", "HEAD")
    commit = head.stdout.strip() if head.returncode == 0 else "UNKNOWN"

    branch = run_git(root, "branch", "--show-current")
    branch_name = branch.stdout.strip() or "(detached HEAD)"

    print("=" * 72)
    print(f"OSBB Assistant v{VERSION}")
    print("=" * 72)
    print(f"Project : {root}")
    print(f"Branch  : {branch_name}")
    print(f"Git HEAD: {commit}")
    print()


def status_line(label: str, value: str, ok: bool | None = None) -> None:
    marker = "[ OK ]" if ok is True else "[FAIL]" if ok is False else "      "
    print(f"{marker} {label:<24} {value}")


def git_worktree_state(root: Path) -> tuple[str, bool]:
    result = run_git(root, "status", "--porcelain")
    if result.returncode != 0:
        return "GIT ERROR", False
    clean = not result.stdout.strip()
    return ("CLEAN" if clean else "MODIFIED"), clean


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
    print("Проверка завершена с ошибками." if failed else "Проверка окружения завершена успешно.")
    return 1 if failed else 0


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
    status_line("Backup directory", str(BACKUP_ROOT), True)

    failed = False
    print()

    for name, rel in TRACKED_FILES.items():
        path = root / rel
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            failed = True
            continue

        info = file_info(path)
        lines = "?" if info["lines"] is None else f'{info["lines"]:,}'
        status_line(name, "OK", True)
        print(f"      Path   : {rel}")
        print(f"      Size   : {info['size_bytes']:,} bytes")
        print(f"      Lines  : {lines}")
        print(f"      SHA256 : {info['sha256']}")

    print()
    print("Doctor обнаружил проблемы." if failed else "Doctor завершил диагностику.")
    return 1 if failed else 0


def cmd_report(root: Path, _args: argparse.Namespace) -> int:
    print_header(root)

    state, clean = git_worktree_state(root)
    branch = run_git(root, "branch", "--show-current")
    branch_name = branch.stdout.strip() or "(detached HEAD)"

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

    status = run_git(root, "status", "--short")
    print("Git status:")
    print(status.stdout.rstrip() or "  clean")
    print()
    print("Этот отчёт можно целиком копировать в рабочий чат.")
    return 0


def cmd_hash(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    failed = False
    for name, path in resolve_tracked_files(args.file, root):
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            failed = True
            continue

        info = file_info(path)
        print(name)
        print(f"  path    : {path.relative_to(root)}")
        print(f"  sha256  : {info['sha256']}")
        print(f"  size    : {info['size_bytes']:,} bytes")
        print(f"  lines   : {info['lines'] if info['lines'] is not None else '?'}")
        print()

    return 1 if failed else 0


def git_blob_hash(root: Path, rel: Path) -> str | None:
    result = run_git(root, "rev-parse", f"HEAD:{rel.as_posix()}")
    return result.stdout.strip() if result.returncode == 0 else None


def local_blob_hash(root: Path, path: Path) -> str | None:
    result = run_git(root, "hash-object", str(path))
    return result.stdout.strip() if result.returncode == 0 else None


def cmd_compare(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    overall_ok = True
    for name, path in resolve_tracked_files(args.file, root):
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            overall_ok = False
            continue

        rel = path.relative_to(root)
        head_blob = git_blob_hash(root, rel)
        local_blob = local_blob_hash(root, path)
        identical = bool(head_blob and local_blob and head_blob == local_blob)

        print(name)
        print(f"  path       : {rel}")
        print(f"  HEAD blob  : {head_blob or 'NOT IN HEAD'}")
        print(f"  Local blob : {local_blob or 'ERROR'}")
        print(f"  result     : {'IDENTICAL' if identical else 'DIFFERS'}")
        print()

        overall_ok = overall_ok and identical

    return 0 if overall_ok else 2


def cmd_backup(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / timestamp
    copied = 0

    for name, source in resolve_tracked_files(args.file, root):
        if not source.exists():
            status_line(name, "NOT FOUND", False)
            continue

        rel = source.relative_to(root)
        destination = backup_dir / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        status_line(name, str(destination), True)
        copied += 1

    print()
    if copied == 0:
        print("Нет файлов для резервного копирования.")
        return 1

    print(f"Создано резервных копий: {copied}")
    print(f"Каталог: {backup_dir}")
    return 0


def cmd_diff(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    git_args = ["diff", "--"]
    if args.file:
        git_args.extend(
            str(path.relative_to(root))
            for _, path in resolve_tracked_files(args.file, root)
        )

    result = run_git(root, *git_args)
    if result.returncode not in {0, 1}:
        print(result.stderr.rstrip(), file=sys.stderr)
        return result.returncode

    print(result.stdout, end="" if result.stdout else "")
    if not result.stdout:
        print("Изменений нет.")
    return 0


def cmd_log(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    result = run_git(
        root,
        "log",
        f"-n{args.count}",
        "--date=short",
        "--pretty=format:%h  %ad  %s",
    )
    if result.returncode != 0:
        print(result.stderr.rstrip(), file=sys.stderr)
        return result.returncode

    print(result.stdout.rstrip() or "История коммитов пуста.")
    return 0


def cmd_apply(root: Path, args: argparse.Namespace) -> int:
    print_header(root)

    patch = Path(args.patch).expanduser()
    if not patch.is_absolute():
        patch = (Path.cwd() / patch).resolve()
    else:
        patch = patch.resolve()

    if not patch.is_file():
        raise AssistantError(f"Patch-файл не найден: {patch}")

    print(f"Patch: {patch}")
    print()

    check = run_git(root, "apply", "--check", str(patch))
    if check.returncode != 0:
        if check.stdout.strip():
            print(check.stdout.rstrip())
        if check.stderr.strip():
            print(check.stderr.rstrip(), file=sys.stderr)
        raise AssistantError("Patch не прошёл git apply --check. Проект не изменён.")

    status_line("git apply --check", "PASSED", True)

    if args.check:
        print()
        print("Проверка завершена. Проект не изменён.")
        return 0

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / f"before_patch_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    status = run_git(root, "status", "--porcelain")
    (backup_dir / "git_status_before.txt").write_text(status.stdout, encoding="utf-8")
    shutil.copy2(patch, backup_dir / patch.name)

    applied = run_git(root, "apply", str(patch))
    if applied.returncode != 0:
        if applied.stdout.strip():
            print(applied.stdout.rstrip())
        if applied.stderr.strip():
            print(applied.stderr.rstrip(), file=sys.stderr)
        raise AssistantError("Git не смог применить patch.")

    status_line("git apply", "APPLIED", True)
    print(f"Служебная копия: {backup_dir}")
    print()
    print("Следующая проверка:")
    print("  python Assistant.py diff")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="assistant",
        description="OSBB Utility Assistant v0.4",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Проверить структуру проекта.")
    sub.add_parser("doctor", help="Выполнить подробную диагностику.")
    sub.add_parser("report", help="Сформировать отчёт для рабочего чата.")

    hash_parser = sub.add_parser("hash", help="Показать SHA256 файлов.")
    hash_parser.add_argument("file", nargs="?")

    compare_parser = sub.add_parser("compare", help="Сравнить с Git HEAD.")
    compare_parser.add_argument("file", nargs="?")

    backup_parser = sub.add_parser("backup", help="Создать резервную копию.")
    backup_parser.add_argument("file", nargs="?")

    diff_parser = sub.add_parser("diff", help="Показать git diff.")
    diff_parser.add_argument("file", nargs="?")

    log_parser = sub.add_parser("log", help="Показать последние коммиты.")
    log_parser.add_argument("-n", "--count", type=int, default=10)

    apply_parser = sub.add_parser("apply", help="Проверить и применить patch.")
    apply_parser.add_argument("patch")
    apply_parser.add_argument("--check", action="store_true")

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
            "backup": cmd_backup,
            "diff": cmd_diff,
            "log": cmd_log,
            "apply": cmd_apply,
        }
        return commands[args.command](root, args)

    except AssistantError as exc:
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
