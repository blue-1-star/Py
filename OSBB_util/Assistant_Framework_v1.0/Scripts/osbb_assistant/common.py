from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

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
    candidates.extend([script_dir, *script_dir.parents, DEFAULT_ROOT])

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


def git_head(root: Path) -> str:
    result = run_git(root, "rev-parse", "--short=12", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else "UNKNOWN"


def print_header(root: Path, version: str) -> None:
    print("=" * 68)
    print(f"OSBB Assistant v{version}")
    print("=" * 68)
    print(f"Project  : {root}")
    print(f"Git HEAD : {git_head(root)}")
    print()


def status_line(label: str, value: str, ok: bool | None = None) -> None:
    marker = "[ OK ]" if ok is True else "[FAIL]" if ok is False else "      "
    print(f"{marker} {label:<22} {value}")


def git_worktree_state(root: Path) -> tuple[str, bool]:
    result = run_git(root, "status", "--porcelain")
    if result.returncode != 0:
        return "GIT ERROR", False
    clean = not result.stdout.strip()
    return ("CLEAN" if clean else "MODIFIED"), clean
