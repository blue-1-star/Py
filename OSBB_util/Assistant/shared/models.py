"""Модели данных OSBB Assistant.

Создано автоматически миграцией MIG-003.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


class ProcessResult:
    """
    Результат выполнения внешней команды.
    """

    command: tuple[str, ...]
    return_code: int
    stdout: str
    stderr: str

    @property
    def success(self) -> bool:
        """
        Команда завершилась с кодом 0.
        """

        return self.return_code == 0

class CheckResult:
    """
    Результат одной проверки.
    """

    section: str
    name: str
    success: bool
    message: str
    path: Path | None = None

    @property
    def status_text(self) -> str:
        """
        Короткий текст статуса.
        """

        return "OK" if self.success else "ERROR"

class ProjectRequirement:
    """
    Описание обязательного или рекомендуемого объекта проекта.
    """

    name: str
    relative_paths: tuple[Path, ...]
    required: bool = True
    object_type: str = "file"

    def __post_init__(self) -> None:
        if not self.relative_paths:
            raise ValueError(
                "ProjectRequirement должен содержать хотя бы один путь."
            )

        if self.object_type not in {"file", "directory"}:
            raise ValueError(
                "object_type должен быть 'file' или 'directory'."
            )

class GitFileStatus:
    """
    Состояние одного файла в выводе git status --porcelain.
    """

    index_status: str
    worktree_status: str
    path: str
    original_path: str | None = None

    @property
    def code(self) -> str:
        """
        Двухсимвольный код Git.
        """

        return f"{self.index_status}{self.worktree_status}"

    @property
    def is_untracked(self) -> bool:
        """
        Файл ещё не отслеживается Git.
        """

        return self.code == "??"

    @property
    def is_ignored(self) -> bool:
        """
        Файл игнорируется Git.
        """

        return self.code == "!!"

    @property
    def is_conflicted(self) -> bool:
        """
        Файл находится в состоянии конфликта.
        """

        return self.code in {
            "DD",
            "AU",
            "UD",
            "UA",
            "DU",
            "AA",
            "UU",
        }

    @property
    def is_renamed(self) -> bool:
        """
        Файл был переименован.
        """

        return (
            self.index_status == "R"
            or self.worktree_status == "R"
        )

    @property
    def is_copied(self) -> bool:
        """
        Файл был скопирован.
        """

        return (
            self.index_status == "C"
            or self.worktree_status == "C"
        )

    @property
    def is_deleted(self) -> bool:
        """
        Файл был удалён.
        """

        return (
            self.index_status == "D"
            or self.worktree_status == "D"
        )

    @property
    def is_added(self) -> bool:
        """
        Новый файл уже добавлен в индекс.
        """

        return self.index_status == "A"

    @property
    def is_modified(self) -> bool:
        """
        Отслеживаемый файл изменён.
        """

        return (
            self.index_status == "M"
            or self.worktree_status == "M"
        )

    @property
    def is_staged(self) -> bool:
        """
        Изменение присутствует в индексе Git.
        """

        return self.index_status not in {" ", "?", "!"}

    @property
    def display_path(self) -> str:
        """
        Представление пути для человека.
        """

        if self.original_path:
            return f"{self.original_path} -> {self.path}"

        return self.path

    @property
    def category(self) -> str:
        """
        Человекочитаемая категория изменения.
        """

        if self.is_conflicted:
            return "conflicted"

        if self.is_untracked:
            return "untracked"

        if self.is_ignored:
            return "ignored"

        if self.is_renamed:
            return "renamed"

        if self.is_copied:
            return "copied"

        if self.is_deleted:
            return "deleted"

        if self.is_added:
            return "added"

        if self.is_modified:
            return "modified"

        return "other"

class GitSummary:
    """
    Сводная информация о Git-репозитории.
    """

    git_version: str
    branch: str
    full_head: str
    short_head: str
    files: tuple[GitFileStatus, ...]

    @property
    def is_clean(self) -> bool:
        """
        Рабочее дерево не содержит изменений.
        """

        return not self.files

    @property
    def changed_count(self) -> int:
        """
        Количество изменённых путей.
        """

        return len(self.files)

    @property
    def conflicted_count(self) -> int:
        """
        Количество конфликтующих путей.
        """

        return sum(item.is_conflicted for item in self.files)

    @property
    def untracked_count(self) -> int:
        """
        Количество неотслеживаемых путей.
        """

        return sum(item.is_untracked for item in self.files)

class DiffFileStat:
    """Статистика изменений одного файла в Git diff."""

    path: str
    added: int | None
    deleted: int | None
    binary: bool = False

    @property
    def changed(self) -> int | None:
        """Общее число изменённых строк, если файл текстовый."""

        if self.added is None or self.deleted is None:
            return None
        return self.added + self.deleted

class DiffSymbol:
    """Объявление Python-класса или функции, найденное в patch."""

    path: str
    kind: str
    name: str
    line: str

class DiffAnalysis:
    """Полный результат анализа Git diff."""

    patch: str
    files: tuple[DiffFileStat, ...]
    symbols: tuple[DiffSymbol, ...]
    staged: bool
    paths: tuple[str, ...]
    untracked: tuple[str, ...]

    @property
    def added_lines(self) -> int:
        return sum(item.added or 0 for item in self.files)

    @property
    def deleted_lines(self) -> int:
        return sum(item.deleted or 0 for item in self.files)

    @property
    def binary_count(self) -> int:
        return sum(item.binary for item in self.files)

class RegisteredCommand:
    """
    Зарегистрированная команда Assistant.
    """

    name: str
    handler: Callable[[argparse.Namespace], int]

__all__ = (
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
