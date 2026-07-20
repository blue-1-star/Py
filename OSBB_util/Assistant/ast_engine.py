#!/usr/bin/env python3
"""AST-движок рефакторинга OSBB Assistant."""

from __future__ import annotations

import ast
import os
import py_compile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SourceRange:
    """Диапазон символов в исходном тексте."""

    start: int
    end: int

    def validate(self, source_length: int) -> None:
        if self.start < 0:
            raise ValueError("Начало диапазона меньше нуля.")

        if self.end < self.start:
            raise ValueError("Конец диапазона меньше начала.")

        if self.end > source_length:
            raise ValueError("Диапазон выходит за пределы исходного текста.")


@dataclass(frozen=True, slots=True)
class ParsedModule:
    """AST вместе с исходным текстом файла."""

    source: str
    tree: ast.Module
    path: Path | None = None

    def node_range(self, node: ast.AST) -> SourceRange:
        required = (
            "lineno",
            "col_offset",
            "end_lineno",
            "end_col_offset",
        )

        if any(not hasattr(node, field) for field in required):
            raise ValueError(
                f"Узел {type(node).__name__} не содержит координат исходного кода."
            )

        offsets = line_offsets(self.source)

        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset

        result = SourceRange(start=start, end=end)
        result.validate(len(self.source))

        return result

    def segment(self, node: ast.AST) -> str:
        source_range = self.node_range(node)

        return self.source[source_range.start : source_range.end]


@dataclass(frozen=True, slots=True)
class SourceEdit:
    """Одна операция замены исходного текста."""

    source_range: SourceRange
    replacement: str
    label: str = ""


@dataclass(frozen=True, slots=True)
class CompileResult:
    """Результат проверки Python-файла."""

    path: Path
    success: bool
    error: str | None = None


def parse_source(
    source: str,
    *,
    filename: str = "<string>",
) -> ParsedModule:
    """Разобрать Python-код в AST."""

    tree = ast.parse(
        source,
        filename=filename,
        type_comments=True,
    )

    return ParsedModule(
        source=source,
        tree=tree,
    )


def parse_file(
    path: str | Path,
    *,
    encoding: str = "utf-8",
) -> ParsedModule:
    """Прочитать и разобрать Python-файл."""

    file_path = Path(path).resolve()
    source = file_path.read_text(encoding=encoding)

    parsed = parse_source(
        source,
        filename=str(file_path),
    )

    return ParsedModule(
        source=parsed.source,
        tree=parsed.tree,
        path=file_path,
    )


def line_offsets(source: str) -> list[int]:
    """Получить позицию начала каждой строки."""

    offsets = [0]

    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))

    return offsets


def decorator_name(decorator: ast.expr) -> str | None:
    """Получить имя декоратора, включая составное имя."""

    if isinstance(decorator, ast.Name):
        return decorator.id

    if isinstance(decorator, ast.Attribute):
        parts: list[str] = []
        current: ast.expr = decorator

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)

            return ".".join(reversed(parts))

    if isinstance(decorator, ast.Call):
        return decorator_name(decorator.func)

    return None


def is_dataclass(node: ast.ClassDef) -> bool:
    """Проверить наличие декоратора dataclass."""

    names = {
        decorator_name(decorator)
        for decorator in node.decorator_list
    }

    return bool(
        names
        & {
            "dataclass",
            "dataclasses.dataclass",
        }
    )


def class_has_methods(
    node: ast.ClassDef,
    *,
    include_dunder: bool = True,
) -> bool:
    """Проверить, содержит ли класс методы."""

    for item in node.body:
        if not isinstance(
            item,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            continue

        if include_dunder:
            return True

        if not (
            item.name.startswith("__")
            and item.name.endswith("__")
        ):
            return True

    return False


def find_classes(
    tree: ast.AST,
    *,
    recursive: bool = False,
) -> list[ast.ClassDef]:
    """Найти классы в AST."""

    if recursive:
        return [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

    return [
        node
        for node in getattr(tree, "body", ())
        if isinstance(node, ast.ClassDef)
    ]


def find_dataclasses(
    tree: ast.AST,
    *,
    pure_only: bool = False,
    excluded_names: Iterable[str] = (),
) -> list[ast.ClassDef]:
    """Найти dataclass-классы."""

    excluded = set(excluded_names)
    result: list[ast.ClassDef] = []

    for node in find_classes(tree):
        if node.name in excluded:
            continue

        if not is_dataclass(node):
            continue

        if pure_only and class_has_methods(node):
            continue

        result.append(node)

    return result


def find_functions(
    tree: ast.AST,
    *,
    recursive: bool = False,
) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Найти функции в AST."""

    function_types = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
    )

    if recursive:
        return [
            node
            for node in ast.walk(tree)
            if isinstance(node, function_types)
        ]

    return [
        node
        for node in getattr(tree, "body", ())
        if isinstance(node, function_types)
    ]


def extract_nodes(
    parsed: ParsedModule,
    nodes: Iterable[ast.AST],
    *,
    separator: str = "\n\n",
) -> str:
    """Извлечь оригинальный текст выбранных AST-узлов."""

    ordered = sorted(
        nodes,
        key=lambda node: parsed.node_range(node).start,
    )

    fragments = [
        parsed.segment(node).rstrip()
        for node in ordered
    ]

    if not fragments:
        return ""

    return separator.join(fragments) + "\n"


def apply_edits(
    source: str,
    edits: Iterable[SourceEdit],
) -> str:
    """Применить непересекающиеся изменения к исходному тексту."""

    ordered = sorted(
        edits,
        key=lambda edit: (
            edit.source_range.start,
            edit.source_range.end,
        ),
    )

    previous_end = 0

    for edit in ordered:
        edit.source_range.validate(len(source))

        if edit.source_range.start < previous_end:
            raise ValueError(
                f"Изменения пересекаются: {edit.label or edit}"
            )

        previous_end = edit.source_range.end

    result = source

    for edit in reversed(ordered):
        start = edit.source_range.start
        end = edit.source_range.end

        result = (
            result[:start]
            + edit.replacement
            + result[end:]
        )

    return result


def remove_nodes(
    parsed: ParsedModule,
    nodes: Iterable[ast.AST],
) -> str:
    """Удалить AST-узлы из исходного текста."""

    edits: list[SourceEdit] = []

    for node in nodes:
        source_range = parsed.node_range(node)
        end = source_range.end

        while (
            end < len(parsed.source)
            and parsed.source[end] == "\n"
        ):
            end += 1

            if end < len(parsed.source):
                if parsed.source[end] != "\n":
                    break

        edits.append(
            SourceEdit(
                source_range=SourceRange(
                    source_range.start,
                    end,
                ),
                replacement="",
                label=f"remove {type(node).__name__}",
            )
        )

    return apply_edits(parsed.source, edits)


def add_from_import(
    parsed: ParsedModule,
    module: str,
    names: Iterable[str],
) -> str:
    """Добавить импорт или расширить существующий from-import."""

    requested = list(dict.fromkeys(names))

    if not requested:
        return parsed.source

    for node in parsed.tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue

        if node.module != module or node.level != 0:
            continue

        existing = [alias.name for alias in node.names]

        missing = [
            name
            for name in requested
            if name not in existing
        ]

        if not missing:
            return parsed.source

        replacement = (
            f"from {module} import "
            + ", ".join(existing + missing)
        )

        return apply_edits(
            parsed.source,
            [
                SourceEdit(
                    source_range=parsed.node_range(node),
                    replacement=replacement,
                    label=f"extend import {module}",
                )
            ],
        )

    insertion_offset = import_insertion_offset(parsed)

    import_line = (
        f"from {module} import "
        + ", ".join(requested)
        + "\n"
    )

    return apply_edits(
        parsed.source,
        [
            SourceEdit(
                source_range=SourceRange(
                    insertion_offset,
                    insertion_offset,
                ),
                replacement=import_line,
                label=f"add import {module}",
            )
        ],
    )


def remove_import_name(
    parsed: ParsedModule,
    module: str,
    name: str,
) -> str:
    """Удалить одно имя из from-import."""

    for node in parsed.tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue

        if node.module != module or node.level != 0:
            continue

        remaining = [
            alias
            for alias in node.names
            if alias.name != name
        ]

        if len(remaining) == len(node.names):
            return parsed.source

        source_range = parsed.node_range(node)

        if remaining:
            rendered = ", ".join(
                (
                    f"{alias.name} as {alias.asname}"
                    if alias.asname
                    else alias.name
                )
                for alias in remaining
            )

            replacement = f"from {module} import {rendered}"

        else:
            replacement = ""

            if (
                source_range.end < len(parsed.source)
                and parsed.source[source_range.end] == "\n"
            ):
                source_range = SourceRange(
                    source_range.start,
                    source_range.end + 1,
                )

        return apply_edits(
            parsed.source,
            [
                SourceEdit(
                    source_range=source_range,
                    replacement=replacement,
                    label=f"remove import {name}",
                )
            ],
        )

    return parsed.source


def import_insertion_offset(parsed: ParsedModule) -> int:
    """Определить безопасное место для нового импорта."""

    body = parsed.tree.body
    offset = 0
    index = 0

    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        offset = parsed.node_range(body[0]).end
        index = 1

        if (
            offset < len(parsed.source)
            and parsed.source[offset] == "\n"
        ):
            offset += 1

    while index < len(body):
        node = body[index]

        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            break

        offset = parsed.node_range(node).end

        if (
            offset < len(parsed.source)
            and parsed.source[offset] == "\n"
        ):
            offset += 1

        index += 1

    return offset


def write_text_atomic(
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
) -> None:
    """Безопасно заменить файл через временный файл."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
        text=True,
    )

    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(
            descriptor,
            "w",
            encoding=encoding,
            newline="",
        ) as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())

        temporary_path.replace(target)

    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def compile_files(
    paths: Iterable[str | Path],
) -> list[CompileResult]:
    """Проверить синтаксис Python-файлов."""

    results: list[CompileResult] = []

    for item in paths:
        path = Path(item).resolve()

        try:
            py_compile.compile(
                str(path),
                doraise=True,
            )

        except py_compile.PyCompileError as error:
            results.append(
                CompileResult(
                    path=path,
                    success=False,
                    error=str(error),
                )
            )

        else:
            results.append(
                CompileResult(
                    path=path,
                    success=True,
                )
            )

    return results