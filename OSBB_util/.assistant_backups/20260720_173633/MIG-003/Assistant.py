#!/usr/bin/env python3
"""
OSBB Assistant 1.0

Служебная консольная утилита для сопровождения проекта OSBB.

Ожидаемая структура:

    G:\\Programming\\Py
    ├── .git
    ├── OSBB
    └── OSBB_util
        └── Scripts
            └── Assistant.py

Assistant расположен вне каталога OSBB и обслуживает проект,
не являясь частью его прикладного кода.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


APP_NAME = "OSBB Assistant"
APP_VERSION = "1.0.0-dev.4"
MINIMUM_PYTHON_VERSION = (3, 10)
SEPARATOR_WIDTH = 72


class AssistantError(Exception):
    """
    Базовая ожидаемая ошибка Assistant.

    Такие ошибки выводятся без полного traceback.
    """


class ConfigurationError(AssistantError):
    """
    Ошибка конфигурации или структуры каталогов.
    """


class CommandExecutionError(AssistantError):
    """
    Ошибка выполнения внешней команды.
    """


class GitRepositoryError(AssistantError):
    """
    Ошибка работы с Git-репозиторием.
    """


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    """
    Пути, используемые Assistant.
    """

    assistant_file: Path
    scripts_dir: Path
    utility_dir: Path
    repository_root: Path
    project_dir: Path
    git_dir: Path

    @classmethod
    def discover(cls) -> "ProjectPaths":
        """
        Определить структуру каталогов относительно Assistant.py.

        Ожидаемое расположение:

            <repository_root>/OSBB_util/Scripts/Assistant.py
        """

        assistant_file = Path(__file__).resolve()
        scripts_dir = assistant_file.parent
        utility_dir = scripts_dir.parent
        repository_root = utility_dir.parent
        project_dir = repository_root / "OSBB"
        git_dir = repository_root / ".git"

        return cls(
            assistant_file=assistant_file,
            scripts_dir=scripts_dir,
            utility_dir=utility_dir,
            repository_root=repository_root,
            project_dir=project_dir,
            git_dir=git_dir,
        )


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
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

@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
class DiffSymbol:
    """Объявление Python-класса или функции, найденное в patch."""

    path: str
    kind: str
    name: str
    line: str


@dataclass(frozen=True, slots=True)
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


@dataclass(frozen=True, slots=True)
class RegisteredCommand:
    """
    Зарегистрированная команда Assistant.
    """

    name: str
    handler: Callable[[argparse.Namespace], int]


class Console:
    """
    Единый интерфейс консольного вывода.
    """

    @staticmethod
    def write(message: str = "") -> None:
        print(message)

    @staticmethod
    def info(message: str) -> None:
        print(f"[INFO]  {message}")

    @staticmethod
    def success(message: str) -> None:
        print(f"[OK]    {message}")

    @staticmethod
    def warning(message: str) -> None:
        print(f"[WARN]  {message}")

    @staticmethod
    def error(message: str) -> None:
        print(f"[ERROR] {message}", file=sys.stderr)

    @staticmethod
    def header(title: str) -> None:
        separator = "=" * SEPARATOR_WIDTH
        print(separator)
        print(title)
        print(separator)

    @staticmethod
    def section(title: str) -> None:
        print()
        print(title)
        print("-" * len(title))


class CommandRunner:
    """
    Безопасный исполнитель внешних процессов.
    """

    def run(
        self,
        command: Sequence[str],
        *,
        cwd: Path,
        check: bool = False,
        timeout: float | None = None,
    ) -> ProcessResult:
        """
        Выполнить внешнюю команду без shell.
        """

        normalized_command = tuple(str(item) for item in command)

        if not normalized_command:
            raise CommandExecutionError(
                "Невозможно выполнить пустую команду."
            )

        if not cwd.exists():
            raise CommandExecutionError(
                f"Рабочий каталог не существует: {cwd}"
            )

        if not cwd.is_dir():
            raise CommandExecutionError(
                f"Рабочий путь не является каталогом: {cwd}"
            )

        try:
            completed = subprocess.run(
                normalized_command,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                shell=False,
                check=False,
            )
        except FileNotFoundError as exc:
            raise CommandExecutionError(
                f"Программа не найдена: {normalized_command[0]}"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            command_text = subprocess.list2cmdline(normalized_command)
            raise CommandExecutionError(
                f"Превышено время выполнения команды: {command_text}"
            ) from exc
        except OSError as exc:
            command_text = subprocess.list2cmdline(normalized_command)
            raise CommandExecutionError(
                f"Не удалось запустить команду: {command_text}. "
                f"Причина: {exc}"
            ) from exc

        result = ProcessResult(
            command=normalized_command,
            return_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

        if check and not result.success:
            command_text = subprocess.list2cmdline(normalized_command)
            details = result.stderr.strip() or result.stdout.strip()

            if details:
                raise CommandExecutionError(
                    f"Команда завершилась с кодом "
                    f"{result.return_code}: {command_text}\n{details}"
                )

            raise CommandExecutionError(
                f"Команда завершилась с кодом "
                f"{result.return_code}: {command_text}"
            )

        return result


class GitRepository:
    """
    Единый интерфейс работы Assistant с Git.

    Остальные компоненты не должны самостоятельно запускать Git.
    """

    def __init__(
        self,
        root: Path,
        runner: CommandRunner,
    ) -> None:
        self.root = root
        self.runner = runner

    def run(
        self,
        arguments: Sequence[str],
        *,
        check: bool = True,
        timeout: float | None = 30.0,
    ) -> ProcessResult:
        """
        Выполнить Git-команду в корне репозитория.
        """

        command = ("git", *arguments)

        try:
            return self.runner.run(
                command,
                cwd=self.root,
                check=check,
                timeout=timeout,
            )
        except CommandExecutionError as exc:
            raise GitRepositoryError(str(exc)) from exc

    def get_git_version(self) -> str:
        """
        Получить строку версии Git.
        """

        result = self.run(
            ("--version",),
            check=True,
            timeout=10.0,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if not output:
            raise GitRepositoryError(
                "Git не вернул информацию о версии."
            )

        return output

    def is_work_tree(self) -> bool:
        """
        Проверить, находится ли путь внутри рабочего дерева Git.
        """

        result = self.run(
            ("rev-parse", "--is-inside-work-tree"),
            check=False,
            timeout=10.0,
        )

        return (
            result.success
            and result.stdout.strip().lower() == "true"
        )

    def get_repository_root(self) -> Path:
        """
        Получить фактический корень рабочего дерева.
        """

        result = self.run(
            ("rev-parse", "--show-toplevel"),
            check=True,
            timeout=10.0,
        )

        raw_path = result.stdout.strip()

        if not raw_path:
            raise GitRepositoryError(
                "Git не вернул корень рабочего дерева."
            )

        return Path(raw_path).resolve()

    def get_branch(self) -> str:
        """
        Получить имя текущей ветки.

        В detached HEAD возвращается специальное обозначение.
        """

        result = self.run(
            ("branch", "--show-current"),
            check=True,
            timeout=10.0,
        )

        branch = result.stdout.strip()

        if branch:
            return branch

        return "(detached HEAD)"

    def get_full_head(self) -> str:
        """
        Получить полный SHA текущего коммита.
        """

        result = self.run(
            ("rev-parse", "HEAD"),
            check=True,
            timeout=10.0,
        )

        head = result.stdout.strip()

        if not head:
            raise GitRepositoryError(
                "Git не вернул SHA текущего коммита."
            )

        return head

    def get_short_head(self) -> str:
        """
        Получить короткий SHA текущего коммита.
        """

        result = self.run(
            ("rev-parse", "--short", "HEAD"),
            check=True,
            timeout=10.0,
        )

        head = result.stdout.strip()

        if not head:
            raise GitRepositoryError(
                "Git не вернул короткий SHA текущего коммита."
            )

        return head

    def get_status_porcelain(self) -> str:
        """
        Получить машинно-читаемый статус рабочего дерева.
        """

        result = self.run(
            (
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ),
            check=True,
            timeout=30.0,
        )

        return result.stdout

    def get_diff(
        self,
        *,
        staged: bool = False,
        paths: Sequence[str] = (),
        timeout: float | None = 60.0,
    ) -> str:
        """Получить unified diff рабочего дерева или индекса."""

        arguments: list[str] = ["diff", "--no-ext-diff", "--no-color"]
        if staged:
            arguments.append("--cached")
        if paths:
            arguments.append("--")
            arguments.extend(paths)

        result = self.run(arguments, check=True, timeout=timeout)
        return result.stdout

    def get_diff_numstat(
        self,
        *,
        staged: bool = False,
        paths: Sequence[str] = (),
        timeout: float | None = 60.0,
    ) -> str:
        """Получить машинно-читаемую статистику Git diff."""

        arguments: list[str] = [
            "diff",
            "--numstat",
            "--no-ext-diff",
            "--no-color",
        ]
        if staged:
            arguments.append("--cached")
        if paths:
            arguments.append("--")
            arguments.extend(paths)

        result = self.run(arguments, check=True, timeout=timeout)
        return result.stdout

    def get_changed_files(self) -> tuple[GitFileStatus, ...]:
        """
        Получить список изменённых файлов.
        """

        output = self.get_status_porcelain()
        items: list[GitFileStatus] = []

        for raw_line in output.splitlines():
            if not raw_line or len(raw_line) < 3:
                continue

            index_status = raw_line[0]
            worktree_status = raw_line[1]
            path_text = raw_line[3:]

            original_path: str | None = None
            current_path = path_text

            if " -> " in path_text:
                original_path, current_path = path_text.split(
                    " -> ",
                    maxsplit=1,
                )

            items.append(
                GitFileStatus(
                    index_status=index_status,
                    worktree_status=worktree_status,
                    path=current_path,
                    original_path=original_path,
                )
            )

        return tuple(items)

    def is_clean(self) -> bool:
        """
        Проверить чистоту рабочего дерева.
        """

        return not self.get_changed_files()

    def get_summary(self) -> GitSummary:
        """
        Получить полную сводку состояния Git.
        """

        return GitSummary(
            git_version=self.get_git_version(),
            branch=self.get_branch(),
            full_head=self.get_full_head(),
            short_head=self.get_short_head(),
            files=self.get_changed_files(),
        )


class DiffAnalyzer:
    """Анализатор Git diff для команд diff, review и doctor."""

    PYTHON_DECLARATION_PREFIXES = (
        "class ",
        "def ",
        "async def ",
    )

    def __init__(self, git: GitRepository) -> None:
        self.git = git

    def analyze(
        self,
        *,
        staged: bool = False,
        paths: Sequence[str] = (),
    ) -> DiffAnalysis:
        """Получить patch, статистику и Python-объявления."""

        normalized_paths = tuple(str(item) for item in paths)
        patch = self.git.get_diff(
            staged=staged,
            paths=normalized_paths,
        )
        numstat = self.git.get_diff_numstat(
            staged=staged,
            paths=normalized_paths,
        )
        files = self._parse_numstat(numstat)
        symbols = self._extract_python_symbols(patch)
        untracked = self._find_untracked(normalized_paths)

        return DiffAnalysis(
            patch=patch,
            files=files,
            symbols=symbols,
            staged=staged,
            paths=normalized_paths,
            untracked=untracked,
        )

    @staticmethod
    def _parse_numstat(output: str) -> tuple[DiffFileStat, ...]:
        items: list[DiffFileStat] = []

        for raw_line in output.splitlines():
            if not raw_line.strip():
                continue

            parts = raw_line.split("\t", maxsplit=2)
            if len(parts) != 3:
                continue

            added_text, deleted_text, path = parts
            binary = added_text == "-" or deleted_text == "-"

            if binary:
                added = None
                deleted = None
            else:
                try:
                    added = int(added_text)
                    deleted = int(deleted_text)
                except ValueError:
                    continue

            items.append(
                DiffFileStat(
                    path=path,
                    added=added,
                    deleted=deleted,
                    binary=binary,
                )
            )

        return tuple(items)

    @classmethod
    def _extract_python_symbols(
        cls,
        patch: str,
    ) -> tuple[DiffSymbol, ...]:
        symbols: list[DiffSymbol] = []
        current_path = ""

        for raw_line in patch.splitlines():
            if raw_line.startswith("+++ b/"):
                current_path = raw_line[6:]
                continue

            if not current_path.endswith(".py"):
                continue

            if not raw_line.startswith("+") or raw_line.startswith("+++"):
                continue

            source_line = raw_line[1:]
            stripped = source_line.lstrip()

            for prefix in cls.PYTHON_DECLARATION_PREFIXES:
                if not stripped.startswith(prefix):
                    continue

                remainder = stripped[len(prefix):]
                name = remainder.split("(", 1)[0].split(":", 1)[0].strip()
                if not name:
                    break

                kind = "class" if prefix == "class " else "function"
                symbols.append(
                    DiffSymbol(
                        path=current_path,
                        kind=kind,
                        name=name,
                        line=stripped,
                    )
                )
                break

        return tuple(symbols)

    def _find_untracked(
        self,
        paths: Sequence[str],
    ) -> tuple[str, ...]:
        selected: list[str] = []

        for item in self.git.get_changed_files():
            if not item.is_untracked:
                continue
            if paths and not self._path_matches(item.path, paths):
                continue
            selected.append(item.path)

        return tuple(sorted(selected, key=str.lower))

    @staticmethod
    def _path_matches(path: str, filters: Sequence[str]) -> bool:
        normalized = path.replace("\\", "/")
        for item in filters:
            candidate = str(item).replace("\\", "/").rstrip("/")
            if normalized == candidate or normalized.startswith(candidate + "/"):
                return True
        return False


class ProjectInspector:
    """
    Проверка структуры проекта OSBB.
    """

    def __init__(self, paths: ProjectPaths) -> None:
        self.paths = paths

    def get_requirements(self) -> tuple[ProjectRequirement, ...]:
        """
        Получить список контролируемых объектов проекта.

        Для файлов, местоположение которых могло меняться,
        допускается несколько возможных относительных путей.
        """

        return (
            ProjectRequirement(
                name="Каталог tools",
                relative_paths=(
                    Path("tools"),
                ),
                required=True,
                object_type="directory",
            ),
            ProjectRequirement(
                name="Каталог cashier_v2_telegram",
                relative_paths=(
                    Path("tools/cashier_v2_telegram"),
                ),
                required=True,
                object_type="directory",
            ),
            ProjectRequirement(
                name="cashier_v2_ui.py",
                relative_paths=(
                    Path(
                        "tools/cashier_v2_telegram/"
                        "cashier_v2_ui.py"
                    ),
                ),
                required=True,
                object_type="file",
            ),
            ProjectRequirement(
                name="cashier_card.py",
                relative_paths=(
                    Path(
                        "tools/cashier_v2_telegram/"
                        "cashier_card.py"
                    ),
                ),
                required=True,
                object_type="file",
            ),
            ProjectRequirement(
                name="Новый слой доступа к БД",
                relative_paths=(
                    Path("core_new/db.access.py"),
                    Path("core_new/db_access.py"),
                    Path("core_new/db/access.py"),
                    Path("db.access.py"),
                    Path("db_access.py"),
                ),
                required=False,
                object_type="file",
            ),
        )

    def inspect(self) -> list[CheckResult]:
        """
        Проверить все зарегистрированные требования.
        """

        results: list[CheckResult] = []

        for requirement in self.get_requirements():
            results.append(
                self._inspect_requirement(requirement)
            )

        return results

    def _inspect_requirement(
        self,
        requirement: ProjectRequirement,
    ) -> CheckResult:
        """
        Проверить один объект проекта.
        """

        for relative_path in requirement.relative_paths:
            absolute_path = (
                self.paths.project_dir / relative_path
            ).resolve()

            if requirement.object_type == "file":
                exists = absolute_path.is_file()
            else:
                exists = absolute_path.is_dir()

            if exists:
                return CheckResult(
                    section="Project",
                    name=requirement.name,
                    success=True,
                    message="найден",
                    path=absolute_path,
                )

        tried_paths = ", ".join(
            str(self.paths.project_dir / item)
            for item in requirement.relative_paths
        )

        if requirement.required:
            return CheckResult(
                section="Project",
                name=requirement.name,
                success=False,
                message=f"не найден; проверены: {tried_paths}",
            )

        return CheckResult(
            section="Project",
            name=requirement.name,
            success=True,
            message=(
                "не найден по известным путям; "
                "проверка пока рекомендательная"
            ),
        )


class CommandRegistry:
    """
    Реестр команд Assistant.
    """

    def __init__(self) -> None:
        self._commands: dict[str, RegisteredCommand] = {}

    def register(
        self,
        name: str,
        handler: Callable[[argparse.Namespace], int],
    ) -> None:
        """
        Зарегистрировать обработчик команды.
        """

        normalized_name = name.strip()

        if not normalized_name:
            raise ConfigurationError(
                "Нельзя зарегистрировать команду без имени."
            )

        if normalized_name in self._commands:
            raise ConfigurationError(
                f"Команда уже зарегистрирована: {normalized_name}"
            )

        self._commands[normalized_name] = RegisteredCommand(
            name=normalized_name,
            handler=handler,
        )

    def execute(
        self,
        name: str,
        args: argparse.Namespace,
    ) -> int:
        """
        Выполнить зарегистрированную команду.
        """

        command = self._commands.get(name)

        if command is None:
            raise AssistantError(
                f"Неизвестная команда: {name}"
            )

        return command.handler(args)

    def names(self) -> tuple[str, ...]:
        """
        Получить имена всех зарегистрированных команд.
        """

        return tuple(sorted(self._commands))


class AssistantApplication:
    """
    Основное приложение OSBB Assistant.
    """

    def __init__(
        self,
        paths: ProjectPaths,
        console: Console,
        runner: CommandRunner,
        git: GitRepository,
        inspector: ProjectInspector,
        diff_analyzer: DiffAnalyzer,
    ) -> None:
        self.paths = paths
        self.console = console
        self.runner = runner
        self.git = git
        self.inspector = inspector
        self.diff_analyzer = diff_analyzer
        self.registry = CommandRegistry()

        self._register_commands()

    def _register_commands(self) -> None:
        """
        Зарегистрировать команды приложения.
        """

        self.registry.register(
            "version",
            self.command_version,
        )
        self.registry.register(
            "paths",
            self.command_paths,
        )
        self.registry.register(
            "check",
            self.command_check,
        )
        self.registry.register(
            "status",
            self.command_status,
        )
        self.registry.register(
            "changes",
            self.command_changes,
        )
        self.registry.register(
            "diff",
            self.command_diff,
        )

    def run_command(
        self,
        command_name: str,
        args: argparse.Namespace,
    ) -> int:
        """
        Выполнить команду через реестр.
        """

        return self.registry.execute(
            command_name,
            args,
        )

    def show_banner(self) -> None:
        """
        Вывести заголовок приложения.
        """

        self.console.header(
            f"{APP_NAME} {APP_VERSION}"
        )

    def show_project_identity(self) -> None:
        """
        Вывести основные пути проекта.
        """

        self.console.write(
            f"Project : {self.paths.project_dir}"
        )
        self.console.write(
            f"Repo    : {self.paths.repository_root}"
        )

    def command_version(
        self,
        args: argparse.Namespace,
    ) -> int:
        """
        Выполнить команду version.
        """

        del args

        self.console.write(
            f"{APP_NAME} {APP_VERSION}"
        )
        self.console.write(
            "Python "
            f"{sys.version_info.major}."
            f"{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        )

        return 0

    def command_paths(
        self,
        args: argparse.Namespace,
    ) -> int:
        """
        Показать рабочие пути.
        """

        del args

        self.show_banner()

        rows = (
            ("Assistant file", self.paths.assistant_file),
            ("Scripts dir", self.paths.scripts_dir),
            ("Utility dir", self.paths.utility_dir),
            ("Repository root", self.paths.repository_root),
            ("Project dir", self.paths.project_dir),
            ("Git dir", self.paths.git_dir),
            ("Current dir", Path.cwd().resolve()),
        )

        width = max(len(label) for label, _ in rows)

        for label, path in rows:
            self.console.write(
                f"{label:<{width}} : {path}"
            )

        return 0

    def command_status(
        self,
        args: argparse.Namespace,
    ) -> int:
        """
        Показать краткое состояние репозитория.
        """

        del args

        self.show_banner()
        self.show_project_identity()

        summary = self.git.get_summary()

        self.console.section("Repository")

        rows = (
            ("Git", summary.git_version),
            ("Branch", summary.branch),
            ("HEAD", summary.short_head),
            (
                "Working tree",
                "clean"
                if summary.is_clean
                else f"modified ({summary.changed_count})",
            ),
            (
                "Untracked",
                str(summary.untracked_count),
            ),
            (
                "Conflicts",
                str(summary.conflicted_count),
            ),
        )

        width = max(len(label) for label, _ in rows)

        for label, value in rows:
            self.console.write(
                f"{label:<{width}} : {value}"
            )

        if summary.files:
            self.console.section("Changed files")

            for item in summary.files:
                self.console.write(
                    f"{item.code}  {item.path}"
                )

        return 1 if summary.conflicted_count else 0

    def command_changes(
        self,
        args: argparse.Namespace,
    ) -> int:
        """
        Показать изменения рабочего дерева,
        сгруппированные по категориям.
        """

        del args

        self.show_banner()
        self.show_project_identity()

        files = self.git.get_changed_files()

        if not files:
            self.console.section("Changes")
            self.console.success(
                "Рабочее дерево чистое. Изменений нет."
            )
            return 0

        groups = self._group_changed_files(files)

        self.console.section("Summary")

        summary_rows = (
            ("Всего путей", len(files)),
            (
                "В индексе",
                sum(item.is_staged for item in files),
            ),
            (
                "Новые",
                sum(item.is_untracked for item in files),
            ),
            (
                "Изменённые",
                sum(item.is_modified for item in files),
            ),
            (
                "Удалённые",
                sum(item.is_deleted for item in files),
            ),
            (
                "Переименованные",
                sum(item.is_renamed for item in files),
            ),
            (
                "Конфликты",
                sum(item.is_conflicted for item in files),
            ),
        )

        width = max(
            len(label)
            for label, _ in summary_rows
        )

        for label, value in summary_rows:
            self.console.write(
                f"{label:<{width}} : {value}"
            )

        section_order = (
            ("conflicted", "Conflicts"),
            ("untracked", "Untracked files"),
            ("added", "Added files"),
            ("modified", "Modified files"),
            ("deleted", "Deleted files"),
            ("renamed", "Renamed files"),
            ("copied", "Copied files"),
            ("other", "Other changes"),
        )

        for category, title in section_order:
            category_files = groups.get(category)

            if not category_files:
                continue

            self.console.section(title)

            for item in category_files:
                staged_marker = (
                    "staged"
                    if item.is_staged
                    else "working tree"
                )

                self.console.write(
                    f"{item.code}  "
                    f"{item.display_path}  "
                    f"[{staged_marker}]"
                )

        conflicted_count = sum(
            item.is_conflicted
            for item in files
        )

        if conflicted_count:
            self.console.write()
            self.console.error(
                "Обнаружены конфликты Git: "
                f"{conflicted_count}."
            )
            return 1

        return 0

    def command_diff(
        self,
        args: argparse.Namespace,
    ) -> int:
        """Показать сводку Git diff и при необходимости полный patch."""

        self.show_banner()
        self.show_project_identity()

        analysis = self.diff_analyzer.analyze(
            staged=bool(args.staged),
            paths=tuple(args.paths or ()),
        )

        self.console.section("Diff")
        self.console.write(
            "Mode    : " + ("staged" if analysis.staged else "working tree")
        )
        self.console.write(
            "Paths   : " + (", ".join(analysis.paths) if analysis.paths else "all")
        )

        self._print_diff_summary(analysis)

        if args.symbols:
            self._print_diff_symbols(analysis)

        if analysis.untracked:
            self.console.section("Untracked files")
            self.console.warning(
                "Эти файлы не входят в обычный git diff, пока не добавлены в индекс."
            )
            for path in analysis.untracked:
                self.console.write(f"??  {path}")

        if args.full:
            self.console.section("Patch")
            if analysis.patch:
                self.console.write(analysis.patch.rstrip())
            else:
                self.console.write("Diff пуст.")

        return 0

    def _print_diff_summary(self, analysis: DiffAnalysis) -> None:
        """Вывести итоговую статистику diff."""

        self.console.section("Summary")
        rows = (
            ("Файлов", len(analysis.files)),
            ("Добавлено строк", analysis.added_lines),
            ("Удалено строк", analysis.deleted_lines),
            ("Бинарных файлов", analysis.binary_count),
            ("Python symbols", len(analysis.symbols)),
        )
        width = max(len(label) for label, _ in rows)
        for label, value in rows:
            self.console.write(f"{label:<{width}} : {value}")

        if not analysis.files:
            self.console.write()
            self.console.success("Изменений в выбранном diff нет.")
            return

        self.console.section("Files")
        for item in analysis.files:
            if item.binary:
                stat = "binary"
            else:
                stat = f"+{item.added} -{item.deleted}"
            self.console.write(f"{stat:<18} {item.path}")

    def _print_diff_symbols(self, analysis: DiffAnalysis) -> None:
        """Вывести найденные объявления Python-классов и функций."""

        self.console.section("Python symbols")
        if not analysis.symbols:
            self.console.write("Новые или изменённые объявления не найдены.")
            return

        for symbol in analysis.symbols:
            self.console.write(
                f"{symbol.kind:<8} {symbol.name:<32} {symbol.path}"
            )

    def command_check(
        self,
        args: argparse.Namespace,
    ) -> int:
        """
        Выполнить расширенную проверку окружения.
        """

        del args

        self.show_banner()
        self.show_project_identity()

        checks = self.collect_checks()
        sections = self._group_checks_by_section(checks)

        for section_name in (
            "Environment",
            "Repository",
            "Project",
        ):
            section_checks = sections.get(section_name)

            if not section_checks:
                continue

            self._print_check_section(
                section_name,
                section_checks,
            )

        failed = [
            item
            for item in checks
            if not item.success
        ]

        self.console.write()
        self.console.write(
            "-" * SEPARATOR_WIDTH
        )

        if failed:
            self.console.error(
                "Проверка завершена с ошибками: "
                f"{len(failed)}."
            )
            return 1

        self.console.success(
            f"Все проверки пройдены: {len(checks)}."
        )
        return 0

    def collect_checks(self) -> list[CheckResult]:
        """
        Собрать результаты всех проверок.
        """

        checks: list[CheckResult] = []

        checks.extend(
            self._collect_environment_checks()
        )
        checks.extend(
            self._collect_repository_checks()
        )
        checks.extend(
            self.inspector.inspect()
        )

        return checks

    def _collect_environment_checks(
        self,
    ) -> list[CheckResult]:
        """
        Проверить Python и каталоги Assistant.
        """

        return [
            self._check_python_version(),
            self._check_directory(
                section="Environment",
                name="Каталог Scripts",
                path=self.paths.scripts_dir,
            ),
            self._check_directory(
                section="Environment",
                name="Каталог OSBB_util",
                path=self.paths.utility_dir,
            ),
            self._check_file(
                section="Environment",
                name="Файл Assistant.py",
                path=self.paths.assistant_file,
            ),
        ]

    def _collect_repository_checks(
        self,
    ) -> list[CheckResult]:
        """
        Проверить структуру и состояние Git.
        """

        checks = [
            self._check_directory(
                section="Repository",
                name="Корень репозитория",
                path=self.paths.repository_root,
            ),
            self._check_directory(
                section="Repository",
                name="Каталог .git",
                path=self.paths.git_dir,
            ),
            self._check_directory(
                section="Repository",
                name="Каталог проекта OSBB",
                path=self.paths.project_dir,
            ),
        ]

        try:
            git_version = self.git.get_git_version()

            checks.append(
                CheckResult(
                    section="Repository",
                    name="Команда Git",
                    success=True,
                    message=git_version,
                )
            )
        except GitRepositoryError as exc:
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Команда Git",
                    success=False,
                    message=str(exc),
                )
            )
            return checks

        try:
            is_work_tree = self.git.is_work_tree()
        except GitRepositoryError as exc:
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Рабочее дерево Git",
                    success=False,
                    message=str(exc),
                )
            )
            return checks

        checks.append(
            CheckResult(
                section="Repository",
                name="Рабочее дерево Git",
                success=is_work_tree,
                message=(
                    "Git-репозиторий подтверждён"
                    if is_work_tree
                    else "Git-репозиторий не подтверждён"
                ),
                path=self.paths.repository_root,
            )
        )

        if not is_work_tree:
            return checks

        try:
            actual_root = self.git.get_repository_root()

            root_matches = (
                actual_root
                == self.paths.repository_root.resolve()
            )

            checks.append(
                CheckResult(
                    section="Repository",
                    name="Корень Git",
                    success=root_matches,
                    message=(
                        "совпадает с ожидаемым"
                        if root_matches
                        else (
                            "не совпадает с ожидаемым: "
                            f"{actual_root}"
                        )
                    ),
                    path=actual_root,
                )
            )
        except GitRepositoryError as exc:
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Корень Git",
                    success=False,
                    message=str(exc),
                )
            )

        try:
            summary = self.git.get_summary()

            checks.append(
                CheckResult(
                    section="Repository",
                    name="Текущая ветка",
                    success=True,
                    message=summary.branch,
                )
            )
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Текущий HEAD",
                    success=True,
                    message=summary.short_head,
                )
            )
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Рабочее состояние",
                    success=(
                        summary.conflicted_count == 0
                    ),
                    message=self._format_work_tree_message(
                        summary
                    ),
                )
            )
        except GitRepositoryError as exc:
            checks.append(
                CheckResult(
                    section="Repository",
                    name="Состояние Git",
                    success=False,
                    message=str(exc),
                )
            )

        return checks

    @staticmethod
    def _format_work_tree_message(
        summary: GitSummary,
    ) -> str:
        """
        Сформировать описание состояния рабочего дерева.
        """

        if summary.is_clean:
            return "clean"

        parts = [
            f"изменено путей: {summary.changed_count}"
        ]

        if summary.untracked_count:
            parts.append(
                f"новых: {summary.untracked_count}"
            )

        if summary.conflicted_count:
            parts.append(
                f"конфликтов: {summary.conflicted_count}"
            )

        return "; ".join(parts)

    @staticmethod
    def _group_checks_by_section(
        checks: Sequence[CheckResult],
    ) -> dict[str, list[CheckResult]]:
        """
        Сгруппировать проверки по разделам.
        """

        grouped: dict[str, list[CheckResult]] = {}

        for item in checks:
            grouped.setdefault(
                item.section,
                [],
            ).append(item)

        return grouped

    def _print_check_section(
        self,
        title: str,
        checks: Sequence[CheckResult],
    ) -> None:
        """
        Вывести раздел результатов проверок.
        """

        self.console.section(title)

        name_width = max(
            len(item.name)
            for item in checks
        )

        for item in checks:
            if item.path is not None:
                message = (
                    f"{item.message}: {item.path}"
                )
            else:
                message = item.message

            self.console.write(
                f"{item.status_text:<5}  "
                f"{item.name:<{name_width}}  "
                f"{message}"
            )

    @staticmethod
    def _group_changed_files(
        files: Sequence[GitFileStatus],
    ) -> dict[str, list[GitFileStatus]]:
        """
        Сгруппировать изменённые файлы
        по человекочитаемым категориям.
        """

        groups: dict[str, list[GitFileStatus]] = {}

        for item in files:
            groups.setdefault(
                item.category,
                [],
            ).append(item)

        for category_files in groups.values():
            category_files.sort(
                key=lambda item: item.display_path.lower()
            )

        return groups

    @staticmethod
    def _check_python_version() -> CheckResult:
        """
        Проверить минимальную версию Python.
        """

        current = (
            sys.version_info.major,
            sys.version_info.minor,
        )

        current_text = (
            f"{sys.version_info.major}."
            f"{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        )

        required_text = ".".join(
            str(item)
            for item in MINIMUM_PYTHON_VERSION
        )

        if current < MINIMUM_PYTHON_VERSION:
            return CheckResult(
                section="Environment",
                name="Версия Python",
                success=False,
                message=(
                    f"Python {current_text}; "
                    f"требуется не ниже {required_text}"
                ),
            )

        return CheckResult(
            section="Environment",
            name="Версия Python",
            success=True,
            message=f"Python {current_text}",
        )

    @staticmethod
    def _check_directory(
        *,
        section: str,
        name: str,
        path: Path,
    ) -> CheckResult:
        """
        Проверить существование каталога.
        """

        if not path.exists():
            return CheckResult(
                section=section,
                name=name,
                success=False,
                message="каталог не найден",
                path=path,
            )

        if not path.is_dir():
            return CheckResult(
                section=section,
                name=name,
                success=False,
                message=(
                    "путь существует, "
                    "но не является каталогом"
                ),
                path=path,
            )

        return CheckResult(
            section=section,
            name=name,
            success=True,
            message="каталог найден",
            path=path,
        )

    @staticmethod
    def _check_file(
        *,
        section: str,
        name: str,
        path: Path,
    ) -> CheckResult:
        """
        Проверить существование файла.
        """

        if not path.exists():
            return CheckResult(
                section=section,
                name=name,
                success=False,
                message="файл не найден",
                path=path,
            )

        if not path.is_file():
            return CheckResult(
                section=section,
                name=name,
                success=False,
                message=(
                    "путь существует, "
                    "но не является файлом"
                ),
                path=path,
            )

        return CheckResult(
            section=section,
            name=name,
            success=True,
            message="файл найден",
            path=path,
        )


def build_parser() -> argparse.ArgumentParser:
    """
    Создать парсер командной строки.
    """

    parser = argparse.ArgumentParser(
        prog="assistant",
        description=(
            "Служебная консольная утилита проекта OSBB."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="команды",
        metavar="COMMAND",
    )

    subparsers.add_parser(
        "version",
        help="показать версию Assistant и Python",
        description=(
            "Показать версию Assistant и Python."
        ),
    )

    subparsers.add_parser(
        "paths",
        help="показать рабочие пути",
        description=(
            "Показать пути проекта, утилиты "
            "и Git-репозитория."
        ),
    )

    subparsers.add_parser(
        "check",
        help="выполнить расширенную проверку",
        description=(
            "Проверить Python, Assistant, Git "
            "и ключевые объекты проекта OSBB."
        ),
    )

    subparsers.add_parser(
        "status",
        help="показать состояние Git-репозитория",
        description=(
            "Показать ветку, HEAD и список "
            "изменённых файлов."
        ),
    )

    subparsers.add_parser(
        "changes",
        help="показать изменённые файлы по категориям",
        description=(
            "Показать новые, изменённые, удалённые, "
            "переименованные и конфликтующие файлы."
        ),
    )

    diff_parser = subparsers.add_parser(
        "diff",
        help="проанализировать изменения Git diff",
        description=(
            "Показать статистику Git diff, изменённые файлы, "
            "Python-объявления и при необходимости полный patch."
        ),
    )
    diff_parser.add_argument(
        "paths",
        nargs="*",
        metavar="PATH",
        help="ограничить diff указанными файлами или каталогами",
    )
    diff_parser.add_argument(
        "--staged",
        "--cached",
        dest="staged",
        action="store_true",
        help="анализировать изменения, добавленные в индекс",
    )
    diff_parser.add_argument(
        "--symbols",
        action="store_true",
        help="показать найденные Python-классы и функции",
    )
    diff_parser.add_argument(
        "--full",
        action="store_true",
        help="вывести полный unified patch",
    )

    return parser


def create_application() -> AssistantApplication:
    """
    Создать приложение и все зависимости.
    """

    paths = ProjectPaths.discover()
    console = Console()
    runner = CommandRunner()
    git = GitRepository(
        root=paths.repository_root,
        runner=runner,
    )
    inspector = ProjectInspector(paths)
    diff_analyzer = DiffAnalyzer(git)

    return AssistantApplication(
        paths=paths,
        console=console,
        runner=runner,
        git=git,
        inspector=inspector,
        diff_analyzer=diff_analyzer,
    )


def dispatch_command(
    app: AssistantApplication,
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> int:
    """
    Передать управление выбранной команде.
    """

    if args.command is None:
        parser.print_help()
        return 0

    return app.run_command(
        args.command,
        args,
    )


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """
    Главная точка входа.
    """

    parser = build_parser()

    try:
        args = parser.parse_args(argv)
        app = create_application()

        return dispatch_command(
            app=app,
            args=args,
            parser=parser,
        )

    except KeyboardInterrupt:
        Console.error(
            "Операция прервана пользователем."
        )
        return 130

    except AssistantError as exc:
        Console.error(str(exc))
        return 1

    except Exception as exc:
        Console.error(
            "Произошла непредвиденная "
            "внутренняя ошибка Assistant."
        )
        Console.error(
            f"{type(exc).__name__}: {exc}"
        )
        Console.error(
            "Сохраните текст ошибки и команду, "
            "которая её вызвала."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())