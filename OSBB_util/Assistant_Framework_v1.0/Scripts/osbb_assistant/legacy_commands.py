from __future__ import annotations

import argparse
import platform
from pathlib import Path

from . import VERSION
from .common import (
    TRACKED_FILES,
    file_info,
    git_worktree_state,
    print_header,
    resolve_tracked_file,
    run_git,
    status_line,
)


def cmd_check(root: Path, _args: argparse.Namespace) -> int:
    print_header(root, VERSION)
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
    print_header(root, VERSION)
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
    print("Doctor обнаружил проблемы." if failed else "Doctor завершил диагностику.")
    return 1 if failed else 0


def cmd_report(root: Path, _args: argparse.Namespace) -> int:
    print_header(root, VERSION)
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
    print("\nЭтот отчёт можно целиком копировать в рабочий чат.")
    return 0


def cmd_hash(root: Path, args: argparse.Namespace) -> int:
    print_header(root, VERSION)
    failed = False
    for name, path in resolve_tracked_file(args.file, root):
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            failed = True
            continue
        info = file_info(path)
        print(name)
        print(f"  path    : {path.relative_to(root)}")
        print(f"  sha256  : {info['sha256']}")
        print(f"  size    : {info['size_bytes']:,} bytes")
        print(f"  lines   : {info['lines'] if info['lines'] is not None else '?'}\n")
    return 1 if failed else 0


def cmd_compare(root: Path, args: argparse.Namespace) -> int:
    print_header(root, VERSION)
    overall_ok = True
    for name, path in resolve_tracked_file(args.file, root):
        rel = path.relative_to(root)
        if not path.exists():
            status_line(name, "NOT FOUND", False)
            overall_ok = False
            continue
        head = run_git(root, "rev-parse", f"HEAD:{rel.as_posix()}")
        local = run_git(root, "hash-object", str(path))
        head_blob = head.stdout.strip() if head.returncode == 0 else None
        local_blob = local.stdout.strip() if local.returncode == 0 else None
        identical = bool(head_blob and local_blob and head_blob == local_blob)
        print(name)
        print(f"  path       : {rel}")
        print(f"  HEAD blob  : {head_blob or 'NOT IN HEAD'}")
        print(f"  Local blob : {local_blob or 'ERROR'}")
        print(f"  result     : {'IDENTICAL' if identical else 'DIFFERS'}\n")
        overall_ok = overall_ok and identical
    return 0 if overall_ok else 2
