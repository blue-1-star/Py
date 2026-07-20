#!/usr/bin/env python3
"""
MIG-003 — Extract Models.

Расположение:
    G:\\Programming\\Py\\OSBB_util\\Scripts\\MIG_003_extract_models.py

Запуск из постоянного рабочего каталога:
    cd /d G:\\Programming\\Py
    python OSBB_util\\Scripts\\MIG_003_extract_models.py

Миграция:
- использует AST-движок OSBB_util/Assistant/ast_engine.py;
- переносит подтверждённые модели из Scripts/Assistant.py;
- оставляет ProjectPaths в точке входа;
- создаёт Assistant/shared/models.py;
- добавляет загрузку пакета Assistant;
- создаёт резервную копию;
- проверяет синтаксис и выполняет smoke-test команд version и paths;
- повторный запуск безопасен.
"""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


MIGRATION_NAME = "MIG-003 — Extract Models"
TARGET_MODEL_NAMES = (
    "ProcessResult",
    "CheckResult",
    "ProjectRequirement",
    "GitFileStatus",
    "GitSummary",
    "DiffFileStat",
    "DiffSymbol",
    "DiffAnalysis",
    "RegisteredCommand",
)
SKIPPED_MODEL_NAMES = ("ProjectPaths",)
PACKAGE_IMPORT_MARKER = "from Assistant.shared.models import ("
PATH_BOOTSTRAP_MARKER = "ASSISTANT_PACKAGE_DIR = Path(__file__).resolve().parent.parent"


def fail(message: str) -> "NoReturn":
    raise RuntimeError(message)


def resolve_layout() -> tuple[Path, Path, Path, Path, Path]:
    migration_file = Path(__file__).resolve()
    scripts_dir = migration_file.parent
    utility_dir = scripts_dir.parent
    repository_root = utility_dir.parent
    assistant_file = scripts_dir / "Assistant.py"
    engine_file = utility_dir / "Assistant" / "ast_engine.py"

    if repository_root != Path(r"G:\Programming\Py"):
        print(
            "[WARN]  Корень отличается от постоянного места: "
            f"{repository_root}"
        )

    if not assistant_file.is_file():
        fail(f"Не найден исходный файл: {assistant_file}")

    if not engine_file.is_file():
        fail(f"Не найден AST-движок: {engine_file}")

    return (
        repository_root,
        utility_dir,
        scripts_dir,
        assistant_file,
        engine_file,
    )


def load_engine(utility_dir: Path):
    utility_text = str(utility_dir)
    if utility_text not in sys.path:
        sys.path.insert(0, utility_text)

    try:
        from Assistant.ast_engine import (  # type: ignore
            ParsedModule,
            SourceEdit,
            SourceRange,
            apply_edits,
            extract_nodes,
            parse_file,
            parse_source,
            write_text_atomic,
        )
    except Exception as exc:
        fail(f"Не удалось загрузить AST-движок: {type(exc).__name__}: {exc}")

    return {
        "ParsedModule": ParsedModule,
        "SourceEdit": SourceEdit,
        "SourceRange": SourceRange,
        "apply_edits": apply_edits,
        "extract_nodes": extract_nodes,
        "parse_file": parse_file,
        "parse_source": parse_source,
        "write_text_atomic": write_text_atomic,
    }


def top_level_classes(tree: ast.Module) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def validate_source(parsed) -> tuple[list[ast.ClassDef], list[str]]:
    classes = top_level_classes(parsed.tree)
    present = [name for name in TARGET_MODEL_NAMES if name in classes]
    missing = [name for name in TARGET_MODEL_NAMES if name not in classes]

    if not present:
        return [], missing

    for name in present:
        node = classes[name]
        decorator_names = {
            _decorator_name(item)
            for item in node.decorator_list
        }
        if not decorator_names.intersection({"dataclass", "dataclasses.dataclass"}):
            fail(f"Класс {name} больше не является dataclass. Миграция остановлена.")

    if "ProjectPaths" not in classes:
        fail("Не найден ProjectPaths; структура Assistant.py изменилась.")

    return [classes[name] for name in present], missing


def _decorator_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts: list[str] = []
        current: ast.expr = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return None


def build_models_source(parsed, nodes, extract_nodes) -> str:
    extracted = extract_nodes(parsed, nodes)

    return (
        '"""Модели данных OSBB Assistant.\n\n'
        "Создано автоматически миграцией MIG-003.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "import argparse\n"
        "from collections.abc import Callable\n"
        "from dataclasses import dataclass\n"
        "from pathlib import Path\n\n\n"
        f"{extracted}"
        "\n__all__ = (\n"
        + "".join(f'    "{name}",\n' for name in TARGET_MODEL_NAMES)
        + ")\n"
    )


def expanded_node_range(parsed, node, SourceRange):
    """
    Возвращает диапазон удаления класса вместе со всеми его декораторами.
    """

    # Если у класса есть декораторы, начинаем удаление с первого из них.
    if node.decorator_list:
        start = parsed.node_range(node.decorator_list[0]).start
    else:
        start = parsed.node_range(node).start

    end = parsed.node_range(node).end

    # Удаляем переводы строк после класса,
    # сохраняя две пустые строки между объявлениями.
    newline_count = 0
    while end < len(parsed.source) and parsed.source[end] in "\r\n":
        if parsed.source[end] == "\n":
            newline_count += 1
        end += 1

    replacement = "\n\n" if newline_count else ""

    return SourceRange(start, end), replacement


def import_insertion_offset(parsed) -> int:
    last_import_end = 0
    for node in parsed.tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import_end = parsed.node_range(node).end
            continue
        if last_import_end:
            break

    if not last_import_end:
        fail("В Assistant.py не найден блок импортов.")

    offset = last_import_end
    while offset < len(parsed.source) and parsed.source[offset] in "\r\n":
        offset += 1
    return offset


def build_assistant_source(parsed, nodes, engine) -> str:
    SourceEdit = engine["SourceEdit"]
    SourceRange = engine["SourceRange"]
    apply_edits = engine["apply_edits"]

    edits = []
    for node in nodes:
        source_range, replacement = expanded_node_range(
            parsed,
            node,
            SourceRange,
        )
        edits.append(
            SourceEdit(
                source_range=source_range,
                replacement=replacement,
                label=f"extract model {node.name}",
            )
        )

    if PACKAGE_IMPORT_MARKER not in parsed.source:
        insertion = import_insertion_offset(parsed)
        import_block = (
            "ASSISTANT_PACKAGE_DIR = Path(__file__).resolve().parent.parent\n"
            "if str(ASSISTANT_PACKAGE_DIR) not in sys.path:\n"
            "    sys.path.insert(0, str(ASSISTANT_PACKAGE_DIR))\n\n"
            "from Assistant.shared.models import (\n"
            + "".join(f"    {name},\n" for name in TARGET_MODEL_NAMES)
            + ")\n\n\n"
        )
        edits.append(
            SourceEdit(
                source_range=SourceRange(insertion, insertion),
                replacement=import_block,
                label="add shared models import",
            )
        )

    return apply_edits(parsed.source, edits)


def ensure_shared_package(utility_dir: Path) -> tuple[Path, Path]:
    shared_dir = utility_dir / "Assistant" / "shared"
    shared_dir.mkdir(parents=True, exist_ok=True)
    init_file = shared_dir / "__init__.py"
    models_file = shared_dir / "models.py"

    if not init_file.exists():
        init_file.write_text(
            '"""Общие компоненты OSBB Assistant."""\n',
            encoding="utf-8",
        )

    return init_file, models_file


def create_backup(
    utility_dir: Path,
    assistant_file: Path,
    models_file: Path,
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = utility_dir / ".assistant_backups" / timestamp / "MIG-003"
    backup_dir.mkdir(parents=True, exist_ok=False)

    shutil.copy2(assistant_file, backup_dir / "Assistant.py")
    if models_file.exists():
        shutil.copy2(models_file, backup_dir / "models.py")

    return backup_dir


def compile_file(path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip()
        fail(f"Синтаксическая проверка не пройдена: {path}\n{details}")


def smoke_test(assistant_file: Path, command: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(assistant_file), command],
        cwd=str(assistant_file.parent.parent.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip()
        fail(f"Smoke-test '{command}' завершился ошибкой:\n{details}")


def restore(
    assistant_file: Path,
    original_assistant: str,
    models_file: Path,
    original_models: str | None,
) -> None:
    assistant_file.write_text(original_assistant, encoding="utf-8", newline="")
    if original_models is None:
        models_file.unlink(missing_ok=True)
    else:
        models_file.write_text(original_models, encoding="utf-8", newline="")


def already_migrated(source: str, models_file: Path) -> bool:
    return (
        PACKAGE_IMPORT_MARKER in source
        and PATH_BOOTSTRAP_MARKER in source
        and models_file.is_file()
        and all(f"class {name}" not in source for name in TARGET_MODEL_NAMES)
    )


def main() -> int:
    print()
    print(MIGRATION_NAME)
    print("=" * 72)

    try:
        (
            repository_root,
            utility_dir,
            _scripts_dir,
            assistant_file,
            _engine_file,
        ) = resolve_layout()
        print(f"Root      : {repository_root}")
        print(f"Assistant : {assistant_file}")

        engine = load_engine(utility_dir)
        parse_file = engine["parse_file"]
        parse_source = engine["parse_source"]
        write_text_atomic = engine["write_text_atomic"]

        _init_file, models_file = ensure_shared_package(utility_dir)
        original_assistant = assistant_file.read_text(encoding="utf-8")
        original_models = (
            models_file.read_text(encoding="utf-8")
            if models_file.exists()
            else None
        )

        if already_migrated(original_assistant, models_file):
            print("\n[1/4] Migration state       ALREADY APPLIED")
            print("[2/4] Compile Assistant.py  ", end="")
            compile_file(assistant_file)
            print("OK")
            print("[3/4] Compile models.py     ", end="")
            compile_file(models_file)
            print("OK")
            print("[4/4] Smoke tests           ", end="")
            smoke_test(assistant_file, "version")
            smoke_test(assistant_file, "paths")
            print("OK")
            print("\nSUCCESS: повторное применение не требуется.")
            return 0

        print("\n[1/7] Parse Assistant.py    ", end="")
        parsed = parse_file(assistant_file)
        nodes, missing = validate_source(parsed)
        print("OK")

        if missing:
            fail(
                "Часть ожидаемых моделей не найдена: "
                + ", ".join(missing)
            )

        print(f"[2/7] Detect models         OK ({len(nodes)} found)")

        models_source = build_models_source(
            parsed,
            nodes,
            engine["extract_nodes"],
        )
        assistant_source = build_assistant_source(parsed, nodes, engine)

        # AST-проверка содержимого до записи на диск.
        parse_source(models_source, filename=str(models_file))
        parse_source(assistant_source, filename=str(assistant_file))

        print("[3/7] Create backup         ", end="")
        backup_dir = create_backup(utility_dir, assistant_file, models_file)
        print(f"OK ({backup_dir})")

        try:
            print("[4/7] Write models.py       ", end="")
            write_text_atomic(models_file, models_source)
            print("OK")

            print("[5/7] Update Assistant.py   ", end="")
            write_text_atomic(assistant_file, assistant_source)
            print("OK")

            print("[6/7] Compile               ", end="")
            compile_file(models_file)
            compile_file(assistant_file)
            print("OK")

            print("[7/7] Smoke tests           ", end="")
            smoke_test(assistant_file, "version")
            smoke_test(assistant_file, "paths")
            print("OK")

        except Exception:
            # restore(
            #     assistant_file,
            #     original_assistant,
            #     models_file,
            #     original_models,
            # )
            print("\n*** RESTORE DISABLED FOR DEBUG ***")
            raise

        print("\nMoved:")
        for name in TARGET_MODEL_NAMES:
            print(f"  {name}")

        print("\nSkipped:")
        for name in SKIPPED_MODEL_NAMES:
            print(f"  {name}")

        print("\nCreated:")
        print(f"  {models_file}")

        print("\nSUCCESS")
        return 0

    except Exception as exc:
        print(f"\nERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
