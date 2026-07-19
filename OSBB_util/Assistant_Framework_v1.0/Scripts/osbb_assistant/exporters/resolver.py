from __future__ import annotations

import argparse
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .. import VERSION
from ..common import git_head, print_header
from ..db_tools import DbCandidate, open_readonly, quote_identifier, resolve_database

RESOLVER_KEYWORDS = (
    "payment", "receipt", "cash", "allocation", "finance", "transaction",
    "apartment", "resident", "owner", "person", "vehicle", "parking", "car",
    "service", "tariff", "account", "balance", "order", "candidate",
)
SENSITIVE_HINTS = (
    "password", "secret", "token", "api_key", "apikey", "hash", "salt",
    "phone", "email", "address", "passport", "tax_id", "inn", "ipn",
)


def _md(value: Any) -> str:
    if value is None:
        return "NULL"
    text = str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ↵ ")
    return text if len(text) <= 180 else text[:177] + "..."


def _is_sensitive(column_name: str) -> bool:
    lowered = column_name.lower()
    return any(hint in lowered for hint in SENSITIVE_HINTS)


def _safe_value(column_name: str, value: Any, include_sensitive: bool) -> Any:
    if include_sensitive or value is None or not _is_sensitive(column_name):
        return value
    return "<REDACTED>"


def _table_names(conn: sqlite3.Connection) -> list[str]:
    return [
        row["name"]
        for row in conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def _objects(conn: sqlite3.Connection, object_type: str) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            "SELECT name, tbl_name, sql FROM sqlite_master "
            "WHERE type=? AND name NOT LIKE 'sqlite_%' ORDER BY name",
            (object_type,),
        )
    )


def _columns(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    return list(conn.execute(f"PRAGMA table_info({quote_identifier(table)})"))


def _foreign_keys(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    return list(conn.execute(f"PRAGMA foreign_key_list({quote_identifier(table)})"))


def _indexes(conn: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    return list(conn.execute(f"PRAGMA index_list({quote_identifier(table)})"))


def _candidate_tables(table_names: Iterable[str], full: bool) -> list[str]:
    names = list(table_names)
    if full:
        return names
    selected = [name for name in names if any(word in name.lower() for word in RESOLVER_KEYWORDS)]
    return selected or names


def _sample_rows(
    conn: sqlite3.Connection,
    table: str,
    limit: int,
    include_sensitive: bool,
) -> tuple[list[str], list[list[Any]], str | None]:
    columns = [row["name"] for row in _columns(conn, table)]
    if not columns:
        return [], [], None
    try:
        query = f"SELECT * FROM {quote_identifier(table)} LIMIT ?"
        rows = list(conn.execute(query, (limit,)))
        cleaned = [
            [_safe_value(column, row[column], include_sensitive) for column in columns]
            for row in rows
        ]
        return columns, cleaned, None
    except sqlite3.Error as exc:
        return columns, [], str(exc)


def _write_table(lines: list[str], headers: list[str], rows: list[list[Any]]) -> None:
    if not headers:
        lines.append("_Нет столбцов._\n")
        return
    lines.append("| " + " | ".join(_md(h) for h in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(_md(v) for v in row) + " |")
    lines.append("")


def _candidate_summary(candidates: list[DbCandidate], selected: Path) -> list[str]:
    lines = ["## Найденные SQLite-базы", ""]
    rows: list[list[Any]] = []
    for item in candidates:
        rows.append([
            "✓" if item.path == selected else "",
            str(item.path),
            item.table_count,
            item.size_bytes,
            datetime.fromtimestamp(item.modified_time).isoformat(timespec="seconds"),
        ])
    _write_table(lines, ["Выбрана", "Путь", "Таблиц", "Размер, байт", "Изменена"], rows)
    return lines


def build_report(
    project_root: Path,
    db_path: Path,
    candidates: list[DbCandidate],
    full: bool,
    sample_limit: int,
    include_data: bool,
    include_sensitive: bool,
) -> str:
    generated = datetime.now().astimezone()
    lines: list[str] = [
        "# OSBB Resolver Export",
        "",
        f"- Создан: `{generated.isoformat(timespec='seconds')}`",
        f"- Assistant: `v{VERSION}`",
        f"- Git HEAD: `{git_head(project_root)}`",
        f"- Проект: `{project_root}`",
        f"- База: `{db_path}`",
        f"- Режим: `{'FULL' if full else 'RESOLVER'}`",
        f"- Образцов на таблицу: `{sample_limit if include_data else 0}`",
        f"- Чувствительные поля: `{'включены' if include_sensitive else 'скрыты'}`",
        "",
    ]
    lines.extend(_candidate_summary(candidates, db_path))

    with open_readonly(db_path) as conn:
        tables = _table_names(conn)
        selected = _candidate_tables(tables, full)
        views = _objects(conn, "view")
        triggers = _objects(conn, "trigger")
        index_objects = _objects(conn, "index")

        lines.extend([
            "## Сводка",
            "",
            f"- Таблиц всего: **{len(tables)}**",
            f"- Таблиц в текущем экспорте: **{len(selected)}**",
            f"- Представлений: **{len(views)}**",
            f"- Триггеров: **{len(triggers)}**",
            f"- Индексов: **{len(index_objects)}**",
            "",
            "## Resolver candidates",
            "",
        ])
        for name in selected:
            lines.append(f"- `{name}`")
        lines.append("")

        lines.extend(["## Карта внешних ключей", ""])
        relation_count = 0
        for table in tables:
            for fk in _foreign_keys(conn, table):
                relation_count += 1
                lines.append(
                    f"- `{table}.{fk['from']}` → `{fk['table']}.{fk['to']}` "
                    f"(on update: `{fk['on_update']}`, on delete: `{fk['on_delete']}`)"
                )
        if relation_count == 0:
            lines.append("_Декларированные FOREIGN KEY не найдены._")
        lines.append("")

        lines.extend(["## Полный список таблиц", ""])
        for name in tables:
            marker = "resolver" if name in selected else "other"
            lines.append(f"- `{name}` — {marker}")
        lines.append("")

        for table in selected:
            lines.extend([f"## Таблица `{table}`", ""])
            create_row = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            lines.extend(["### CREATE TABLE", "", "```sql", (create_row["sql"] if create_row else "-- SQL unavailable"), "```", ""])

            cols = _columns(conn, table)
            col_rows = [[r["cid"], r["name"], r["type"], r["notnull"], r["dflt_value"], r["pk"]] for r in cols]
            lines.extend(["### Столбцы", ""])
            _write_table(lines, ["CID", "Имя", "Тип", "NOT NULL", "DEFAULT", "PK"], col_rows)

            fks = _foreign_keys(conn, table)
            lines.extend(["### Внешние ключи", ""])
            if fks:
                fk_rows = [[r["id"], r["from"], r["table"], r["to"], r["on_update"], r["on_delete"]] for r in fks]
                _write_table(lines, ["ID", "Поле", "Таблица", "Поле назначения", "ON UPDATE", "ON DELETE"], fk_rows)
            else:
                lines.append("_Нет декларированных внешних ключей._\n")

            indexes = _indexes(conn, table)
            lines.extend(["### Индексы", ""])
            if indexes:
                idx_rows = [[r["name"], r["unique"], r["origin"], r["partial"]] for r in indexes]
                _write_table(lines, ["Имя", "UNIQUE", "Origin", "Partial"], idx_rows)
            else:
                lines.append("_Нет индексов._\n")

            if include_data:
                lines.extend([f"### Пример данных (до {sample_limit} строк)", ""])
                headers, rows, error = _sample_rows(conn, table, sample_limit, include_sensitive)
                if error:
                    lines.append(f"_Ошибка чтения образца: `{error}`_\n")
                elif not rows:
                    lines.append("_Таблица пуста._\n")
                else:
                    _write_table(lines, headers, rows)

        for title, objects in (("Представления", views), ("Триггеры", triggers)):
            lines.extend([f"## {title}", ""])
            if not objects:
                lines.append("_Не найдены._\n")
                continue
            for obj in objects:
                lines.extend([f"### `{obj['name']}`", "", "```sql", obj["sql"] or "-- SQL unavailable", "```", ""])

    return "\n".join(lines).rstrip() + "\n"


def run(root: Path, args: argparse.Namespace, script_path: Path) -> int:
    print_header(root, VERSION)
    db_path, candidates = resolve_database(root, args.db)
    output_dir = Path(args.output).expanduser() if args.output else script_path.parent.parent / "Exports"
    if not output_dir.is_absolute():
        output_dir = (Path.cwd() / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_path = output_dir / f"resolver_export_{stamp}.md"
    report = build_report(
        project_root=root,
        db_path=db_path,
        candidates=candidates,
        full=args.full,
        sample_limit=args.samples,
        include_data=not args.no_data,
        include_sensitive=args.include_sensitive,
    )
    output_path.write_text(report, encoding="utf-8")

    print(f"SQLite-база : {db_path}")
    print(f"Отчёт       : {output_path}")
    print(f"Размер       : {output_path.stat().st_size:,} bytes")
    print("\nЭкспорт Resolver завершён успешно.")
    return 0
