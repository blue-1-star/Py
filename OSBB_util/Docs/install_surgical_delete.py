#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

APP_NAME = "OSBB Surgical Delete Document Installer"
APP_VERSION = "1.0.0"
DEFAULT_DATE = "2026-07-24"
DOCUMENT_NAME = "Surgical_Delete.md"
CHRONICLE_MARKER = "surgical-delete-chronicle"
PROJECT_LOG_MARKER = "surgical-delete-project-log"


class InstallerError(Exception):
    pass


@dataclass(frozen=True)
class Paths:
    repository_root: Path
    project_root: Path
    utility_root: Path
    docs_utility_dir: Path
    source_document: Path
    target_document: Path
    chronicle_file: Path
    project_log_file: Path
    backup_dir: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Разместить Surgical_Delete.md и обновить документацию OSBB."
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--date", default=DEFAULT_DATE)
    return parser.parse_args()


def discover_paths(args: argparse.Namespace) -> Paths:
    script_file = Path(__file__).resolve()
    docs_utility_dir = script_file.parent
    utility_root = docs_utility_dir.parent
    repository_root = utility_root.parent
    project_root = (
        args.project_root.expanduser().resolve()
        if args.project_root
        else repository_root / "OSBB"
    )
    source_document = (
        args.source.expanduser().resolve()
        if args.source
        else docs_utility_dir / DOCUMENT_NAME
    )
    target_document = project_root / "Docs" / "Architecture" / DOCUMENT_NAME
    chronicle_file = project_root / "Docs" / "Chronicle" / "2026-07.md"
    project_log_file = project_root / "Docs" / "Project_Log.md"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = utility_root / "Docs" / ".backups" / f"surgical_delete_{timestamp}"
    return Paths(
        repository_root,
        project_root,
        utility_root,
        docs_utility_dir,
        source_document,
        target_document,
        chronicle_file,
        project_log_file,
        backup_dir,
    )


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return normalize(path.read_text(encoding="utf-8-sig"))


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalize(content), encoding="utf-8")


def validate(paths: Paths) -> None:
    if not paths.project_root.is_dir():
        raise InstallerError(f"Каталог проекта OSBB не найден:\n{paths.project_root}")
    if not paths.source_document.is_file():
        raise InstallerError(
            "Готовый документ не найден.\n"
            f"Ожидаемый путь:\n{paths.source_document}\n\n"
            "Помести Surgical_Delete.md рядом со скриптом либо используй --source <путь>."
        )
    text = paths.source_document.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise InstallerError(f"Документ пуст:\n{paths.source_document}")
    if not text.startswith("#"):
        raise InstallerError("Первая непустая строка Surgical_Delete.md должна начинаться с '#'.")


def managed_block(marker: str, body: str) -> str:
    return (
        f"<!-- OSBB-MANAGED:{marker}:BEGIN -->\n"
        f"{body.strip()}\n"
        f"<!-- OSBB-MANAGED:{marker}:END -->"
    )


def upsert(existing: str, marker: str, body: str) -> tuple[str, str]:
    begin = f"<!-- OSBB-MANAGED:{marker}:BEGIN -->"
    end = f"<!-- OSBB-MANAGED:{marker}:END -->"
    block = managed_block(marker, body)
    if begin in existing and end in existing:
        before, tail = existing.split(begin, 1)
        _, after = tail.split(end, 1)
        return normalize(before.rstrip() + "\n\n" + block + after), "UPDATED"
    if existing.strip():
        return normalize(existing.rstrip() + "\n\n" + block), "ADDED"
    return normalize(block), "CREATED"


def copy_document(paths: Paths, dry_run: bool) -> str:
    source = read_text(paths.source_document)
    target = read_text(paths.target_document)
    if target and source == target:
        return "UNCHANGED"
    existed = paths.target_document.exists()
    if existed and not dry_run:
        paths.backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(paths.target_document, paths.backup_dir / DOCUMENT_NAME)
    if not dry_run:
        paths.target_document.parent.mkdir(parents=True, exist_ok=True)
        paths.target_document.write_text(source, encoding="utf-8")
    return "UPDATED" if existed else "CREATED"


def update_chronicle(paths: Paths, date: str, dry_run: bool) -> str:
    existing = read_text(paths.chronicle_file) or "# Летопись OSBB — июль 2026\n"
    body = f'''## {date} — Документирован механизм хирургического удаления

Подготовлен и размещен архитектурный документ:

```text
Docs/Architecture/Surgical_Delete.md
```

Документ фиксирует существующий в OSBB подход к исправлению ошибочных операций:

> В OSBB удаляется не запись базы данных, а ошибочно созданная бизнес-операция.

Описаны назначение механизма, участвующие модули и таблицы, порядок удаления
связанных данных, журналирование действий и требования к сохранению целостности.

Документ появился как результат исследования уже работающего механизма.
Он не вводит новую архитектуру, а сохраняет знание о фактическом устройстве проекта.
'''
    updated, status = upsert(existing, CHRONICLE_MARKER, body)
    write_text(paths.chronicle_file, updated, dry_run)
    return status


def update_project_log(paths: Paths, date: str, dry_run: bool) -> str:
    existing = read_text(paths.project_log_file) or "# Project Log\n"
    body = f'''## {date} — Surgical Delete

В `Docs/Architecture/Surgical_Delete.md` зафиксирован действующий механизм
хирургического удаления ошибочно созданных бизнес-операций.

Документ описывает связанные модули и таблицы, каскадное удаление,
журналирование и контроль целостности данных.
'''
    updated, status = upsert(existing, PROJECT_LOG_MARKER, body)
    write_text(paths.project_log_file, updated, dry_run)
    return status


def verify(paths: Paths) -> list[str]:
    errors: list[str] = []
    for path in (paths.target_document, paths.chronicle_file, paths.project_log_file):
        if not path.is_file():
            errors.append(f"Не создан файл: {path}")
    if paths.target_document.is_file() and read_text(paths.source_document) != read_text(paths.target_document):
        errors.append("Содержимое установленного документа не совпадает с исходным.")
    if paths.chronicle_file.is_file() and CHRONICLE_MARKER not in read_text(paths.chronicle_file):
        errors.append("В Chronicle отсутствует запись Surgical Delete.")
    if paths.project_log_file.is_file() and PROJECT_LOG_MARKER not in read_text(paths.project_log_file):
        errors.append("В Project_Log отсутствует запись Surgical Delete.")
    return errors


def main() -> int:
    args = parse_args()
    paths = discover_paths(args)
    try:
        print("=" * 72)
        print(f"{APP_NAME} {APP_VERSION}")
        print("=" * 72)
        print(f"Mode    : {'DRY RUN' if args.dry_run else 'INSTALL'}")
        print(f"Project : {paths.project_root}")
        print(f"Source  : {paths.source_document}")
        print(f"Target  : {paths.target_document}")
        print()
        validate(paths)
        doc_status = copy_document(paths, args.dry_run)
        chr_status = update_chronicle(paths, args.date, args.dry_run)
        log_status = update_project_log(paths, args.date, args.dry_run)
        print("Planned changes" if args.dry_run else "Completed")
        print("-" * 72)
        print(f"{doc_status:9} {paths.target_document}")
        print(f"{chr_status:9} {paths.chronicle_file}")
        print(f"{log_status:9} {paths.project_log_file}")
        if args.dry_run:
            print("\nФайлы не изменялись.")
            return 0
        errors = verify(paths)
        if errors:
            print("\nVerification: ERROR")
            for error in errors:
                print(f"  - {error}")
            return 2
        print("\nVerification: OK")
        if paths.backup_dir.exists():
            print(f"Backup      : {paths.backup_dir}")
        return 0
    except (InstallerError, OSError, UnicodeError) as exc:
        print("\nERROR")
        print("-" * 72)
        print(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
