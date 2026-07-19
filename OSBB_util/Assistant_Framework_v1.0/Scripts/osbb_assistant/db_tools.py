from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

DB_SUFFIXES = {".db", ".sqlite", ".sqlite3"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "backup", "backups"}


@dataclass(frozen=True)
class DbCandidate:
    path: Path
    table_count: int
    size_bytes: int
    modified_time: float


def quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def inspect_candidate(path: Path) -> DbCandidate | None:
    try:
        uri = f"file:{path.as_posix()}?mode=ro"
        with sqlite3.connect(uri, uri=True, timeout=3) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ).fetchone()[0]
        stat = path.stat()
        return DbCandidate(path, int(count), stat.st_size, stat.st_mtime)
    except (sqlite3.Error, OSError):
        return None


def discover_databases(project_root: Path) -> list[DbCandidate]:
    osbb_root = project_root / "OSBB"
    candidates: list[DbCandidate] = []
    for path in osbb_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in DB_SUFFIXES:
            continue
        if any(part.lower() in SKIP_DIRS for part in path.parts):
            continue
        item = inspect_candidate(path)
        if item is not None:
            candidates.append(item)
    return sorted(
        candidates,
        key=lambda item: (item.table_count, item.modified_time, item.size_bytes),
        reverse=True,
    )


def resolve_database(project_root: Path, requested: str | None) -> tuple[Path, list[DbCandidate]]:
    if requested:
        path = Path(requested).expanduser()
        if not path.is_absolute():
            path = project_root / path
        path = path.resolve()
        if not path.exists():
            raise FileNotFoundError(f"Файл базы данных не найден: {path}")
        inspected = inspect_candidate(path)
        if inspected is None:
            raise ValueError(f"Файл не является доступной SQLite-базой: {path}")
        return path, [inspected]

    candidates = discover_databases(project_root)
    if not candidates:
        raise FileNotFoundError(
            "В каталоге OSBB не найдена доступная SQLite-база (*.db, *.sqlite, *.sqlite3). "
            "Укажите путь явно: assistant export resolver --db <путь>"
        )
    return candidates[0].path, candidates


def open_readonly(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn
