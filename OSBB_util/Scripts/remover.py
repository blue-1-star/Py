"""
AST node removal utilities for OSBB Assistant.

Designed for structural refactorings (MIG-003+).
"""

from __future__ import annotations

from dataclasses import dataclass
import ast
from bisect import bisect_left


@dataclass(frozen=True, slots=True)
class RemovalRange:
    start: int
    end: int


def _line_offsets(text: str) -> list[int]:
    offs = [0]
    pos = 0
    for line in text.splitlines(True):
        pos += len(line)
        offs.append(pos)
    return offs


def _line_to_offset(offsets: list[int], line: int) -> int:
    if line <= 1:
        return 0
    return offsets[line - 1]


def class_range(source: str, node: ast.ClassDef) -> RemovalRange:
    """
    Return removal range including decorators.
    """
    offsets = _line_offsets(source)

    start_line = node.lineno
    if node.decorator_list:
        start_line = min(d.lineno for d in node.decorator_list)

    end_line = node.end_lineno or node.lineno

    lines = source.splitlines(True)

    while end_line < len(lines) and lines[end_line].strip() == "":
        end_line += 1

    return RemovalRange(
        start=_line_to_offset(offsets, start_line),
        end=_line_to_offset(offsets, end_line + 1),
    )


def remove_node(source: str, node: ast.AST) -> str:
    if not hasattr(node, "lineno"):
        raise TypeError("AST node has no coordinates")

    if isinstance(node, ast.ClassDef):
        r = class_range(source, node)
    else:
        offsets = _line_offsets(source)
        start = _line_to_offset(offsets, node.lineno)
        end = _line_to_offset(offsets, (node.end_lineno or node.lineno) + 1)
        r = RemovalRange(start, end)

    return cleanup_blank_lines(source[:r.start] + source[r.end:])


def remove_nodes(source: str, nodes: list[ast.AST]) -> str:
    result = source
    sortable = []
    for n in nodes:
        if isinstance(n, ast.ClassDef):
            rr = class_range(result, n)
            sortable.append((rr.start, rr.end))
    for start, end in sorted(sortable, reverse=True):
        result = cleanup_blank_lines(result[:start] + result[end:])
    return result


def cleanup_blank_lines(text: str) -> str:
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text
