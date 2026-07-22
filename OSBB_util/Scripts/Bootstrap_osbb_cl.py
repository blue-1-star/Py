#!/usr/bin/env python3
"""
bootstrap_osbb_cl.py
=====================

Материализует каркас нового проекта OSBB_cl на диске: создаёт структуру
папок, кладёт config.py и .gitignore, копирует уже подготовленные файлы
(если пути к ним переданы), и инициализирует git-репозиторий с первым
коммитом.

Ничего не берёт из старого OSBB автоматически — только то, что вы явно
укажете через аргументы. Если какой-то путь не передан или не найден —
скрипт просто оставит соответствующую папку пустой (не ошибка, только
предупреждение), чтобы вы могли доложить файлы позже вручную.

Пример запуска (PowerShell):

    python bootstrap_osbb_cl.py `
        --target "G:\\Programming\\OSBB_cl" `
        --db-access "G:\\Programming\\Py\\OSBB_util\\output\\db_access.py" `
        --triage-script "G:\\Programming\\Py\\OSBB_util\\Scripts\\osbb_cleanup_triage.py" `
        --dedupe-script "G:\\Programming\\Py\\OSBB_util\\Scripts\\dedupe_shadowed_functions.py" `
        --harvest-script "G:\\Programming\\Py\\OSBB\\tools\\harvest_lost_features_from_sandboxes.py" `
        --promote-script "G:\\Programming\\Py\\OSBB\\promote_sandbox_to_training_db.py" `
        --dump-script "G:\\Programming\\Py\\OSBB\\tools\\dump_service_codes_live_sandbox.py"

Повторный запуск безопасен: существующие папки не трогаются заново,
уже скопированные файлы не перезаписываются молча (см. --overwrite).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CONFIG_PY_CONTENT = '''# config.py (в корне OSBB_cl/)
#
# Кроссплатформенный конфиг путей, но, в отличие от старого общего
# config.py в Py/, этот — выделенный, только под нужды OSBB_cl.
# Никакого Music/Flat/чужих проектов здесь нет и не будет.

import sys
import platform
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


class ProjectPaths:
    def __init__(self):
        self.os_name = platform.system()
        self.home = Path.home()
        self.PROJECT_ROOT = PROJECT_ROOT

        # ==================================================
        # СЕКРЕТЫ (токен телеграм-бота и т.п.) — вне репозитория
        # ==================================================
        # TODO: подтвердить актуальный путь — сейчас взято по аналогии
        # со старым config.py (G:/Prog_secret на Windows).
        if self.os_name == "Windows":
            self.SECRETS_DIR = Path("G:/Prog_secret")
        else:  # Darwin (Mac) и прочие — единообразно
            self.SECRETS_DIR = self.home / "Programming" / "Secrets"

        self.TELEGRAM_SECRETS_FILE = self.SECRETS_DIR / "telegram_osbb.py"

        # ==================================================
        # ДАННЫЕ
        # ==================================================
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.DB_DIR = self.DATA_DIR / "db"
        self.DB_FILE = self.DB_DIR / "osbb.db"          # бывший osbb_test.db
        self.LOGS_DIR = self.DATA_DIR / "logs"
        self.EXPORTS_DIR = self.DATA_DIR / "exports"      # для отчётов dev_infrastructure

        # ==================================================
        # ПОДСИСТЕМЫ (для удобных импортов и диагностики)
        # ==================================================
        self.CORE_NEW_DIR = self.PROJECT_ROOT / "core_new"
        self.FINANCE_CORE_DIR = self.PROJECT_ROOT / "finance_core"
        self.PRESENTATION_DIR = self.PROJECT_ROOT / "presentation"
        self.DEV_INFRA_DIR = self.PROJECT_ROOT / "dev_infrastructure"

        # ==================================================
        # ДОКУМЕНТАЦИЯ
        # ==================================================
        self.DOCS_DIR = self.PROJECT_ROOT / "docs"

    def ensure_directories(self):
        """Создаёт недостающие рабочие папки (не трогает git/секреты)."""
        dirs = [
            self.DATA_DIR,
            self.DB_DIR,
            self.LOGS_DIR,
            self.EXPORTS_DIR,
            self.DOCS_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)


# ✅ ЕДИНЫЙ ЭКЗЕМПЛЯР — как и в старом config.py
paths = ProjectPaths()
'''

GITIGNORE_CONTENT = '''__pycache__/
*.pyc
.venv/
venv/
*.diff
data/logs/
data/exports/
# Основная БД (data/db/osbb.db) сознательно НЕ игнорируется —
# это единственный источник правды для свежего старта. Если позже
# решите не хранить бинарник в git, раскомментируйте следующую строку:
# data/db/*.db
'''

README_CONTENT = '''# OSBB_cl

Чистый каркас проекта OSBB, выделенный из накопившегося старого дерева
(`G:\\Programming\\Py\\OSBB`) с фокусом на то, что реально нужно для
пилотного запуска Telegram-кассира.

Подсистемы (см. daily handoff от 20.07.2026):
- `core_new/` — новый слой доступа к данным (adapters/, domain/)
- `finance_core/` — финансовое ядро (в т.ч. неразнесённые платежи)
- `presentation/` — пользовательский интерфейс (Telegram-бот)
- `dev_infrastructure/` — инженерные инструменты (диагностика, чистка, дедупликация)

Своя история git, не связана с репозиторием Py/.
'''

# Структура папок. (relative_path, needs_init_py)
DIR_STRUCTURE = [
    ("core_new", True),
    ("core_new/adapters", True),
    ("core_new/domain", True),
    ("finance_core", True),
    ("presentation", True),
    ("presentation/handlers", True),
    ("presentation/cashier_v2_telegram", True),
    ("dev_infrastructure", False),
    ("data", False),
    ("data/db", False),
    ("data/raw", False),
    ("data/raw/typed", False),
    ("data/logs", False),
    ("data/exports", False),
    ("data/reports", False),
    ("migrations", False),
    ("docs", False),
]

# Копирование готовых файлов: (имя аргумента, относительный путь назначения)
COPY_TARGETS = {
    "db_access": "core_new/db_access.py",
    "triage_script": "dev_infrastructure/osbb_cleanup_triage.py",
    "dedupe_script": "dev_infrastructure/dedupe_shadowed_functions.py",
    "harvest_script": "dev_infrastructure/harvest_lost_features_from_sandboxes.py",
    "promote_script": "dev_infrastructure/promote_sandbox_to_training_db.py",
    "dump_script": "dev_infrastructure/dump_service_codes_live_sandbox.py",
}


def run_git(args, cwd, description):
    try:
        result = subprocess.run(
            ["git"] + args, cwd=cwd, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            print(f"  ПРЕДУПРЕЖДЕНИЕ: git {' '.join(args)} завершился с ошибкой:")
            print("   ", result.stderr.strip())
        return result.returncode == 0
    except FileNotFoundError:
        print("  ПРЕДУПРЕЖДЕНИЕ: git не найден в PATH — пропускаю", description)
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, help=r'Куда создавать проект, например "G:\Programming\OSBB_cl"')
    ap.add_argument("--overwrite", action="store_true", help="Перезаписать уже скопированные файлы (по умолчанию — пропускает существующие)")
    ap.add_argument("--no-git", action="store_true", help="Не делать git init/commit")

    for arg_name in COPY_TARGETS:
        ap.add_argument(f"--{arg_name.replace('_', '-')}", default=None,
                         help=f"Путь к готовому файлу для {COPY_TARGETS[arg_name]} (необязательно)")

    args = ap.parse_args()

    target = Path(args.target).resolve()
    print(f"Целевая папка: {target}")
    target.mkdir(parents=True, exist_ok=True)

    # 1) Структура папок
    print("\n=== Создаю структуру папок ===")
    for rel_path, needs_init in DIR_STRUCTURE:
        d = target / rel_path
        d.mkdir(parents=True, exist_ok=True)
        print(f"  {rel_path}/")
        if needs_init:
            init_file = d / "__init__.py"
            if not init_file.exists():
                init_file.write_text("", encoding="utf-8")

    # 2) config.py
    print("\n=== Кладу config.py ===")
    config_path = target / "config.py"
    if config_path.exists() and not args.overwrite:
        print("  config.py уже существует — пропускаю (используйте --overwrite для перезаписи)")
    else:
        config_path.write_text(CONFIG_PY_CONTENT, encoding="utf-8")
        print("  config.py записан")

    # 3) .gitignore
    gitignore_path = target / ".gitignore"
    if gitignore_path.exists() and not args.overwrite:
        print(".gitignore уже существует — пропускаю")
    else:
        gitignore_path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
        print(".gitignore записан")

    # 4) README.md
    readme_path = target / "README.md"
    if not readme_path.exists() or args.overwrite:
        readme_path.write_text(README_CONTENT, encoding="utf-8")

    # 5) requirements.txt (заглушка)
    req_path = target / "requirements.txt"
    if not req_path.exists():
        req_path.write_text("# TODO: заполнить реальными зависимостями (python-telegram-bot и т.п.)\n", encoding="utf-8")

    # 6) Копирование готовых файлов
    print("\n=== Копирую готовые файлы ===")
    copied_count = 0
    for arg_name, rel_dest in COPY_TARGETS.items():
        src_str = getattr(args, arg_name)
        dest = target / rel_dest
        if not src_str:
            print(f"  {rel_dest}: путь не передан — папка остаётся пустой")
            continue
        src = Path(src_str)
        if not src.exists():
            print(f"  {rel_dest}: ПРЕДУПРЕЖДЕНИЕ — файл-источник не найден: {src}")
            continue
        if dest.exists() and not args.overwrite:
            print(f"  {rel_dest}: уже существует — пропускаю (используйте --overwrite для перезаписи)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  {rel_dest}: скопирован из {src}")
        copied_count += 1

    print(f"\nСкопировано файлов: {copied_count} из {len(COPY_TARGETS)}")
    # 6.5) Скрипт кладёт сам себя в dev_infrastructure/ — он и есть
    # зачинатель проекта, его законное место рядом с остальным
    # инструментарием Development Infrastructure.
    self_path = Path(__file__).resolve()
    self_dest = target / "dev_infrastructure" / self_path.name
    if self_dest.exists() and not args.overwrite:
        print(f"\n{self_dest.relative_to(target)} уже существует — пропускаю (используйте --overwrite для перезаписи)")
    else:
        try:
            shutil.copy2(self_path, self_dest)
            print(f"\nСкрипт-зачинатель скопирован в: {self_dest.relative_to(target)}")
        except Exception as e:
            print(f"\nПРЕДУПРЕЖДЕНИЕ: не удалось скопировать сам себя: {e}")

    # 7) git init + commit
    if args.no_git:
        print("\n=== git init/commit пропущен (--no-git) ===")
    else:
        print("\n=== Инициализирую git ===")
        git_dir = target / ".git"
        if git_dir.exists():
            print("  .git уже существует — пропускаю git init")
        else:
            run_git(["init"], target, "git init")

        run_git(["add", "-A"], target, "git add -A")
        committed = run_git(
            ["commit", "-m", "initial import: чистый каркас OSBB_cl (структура, config.py, готовые файлы)"],
            target,
            "git commit",
        )
        if committed:
            print("  Коммит создан.")
        else:
            print("  Коммит не создан (возможно, нечего коммитить, или git не настроен — проверьте user.name/user.email)")

    print(f"\nГотово. Каркас OSBB_cl материализован в: {target}")


if __name__ == "__main__":
    main()

    python "G:\Programming\Py\OSBB_util\Scripts\bootstrap_osbb_cl.py" `
    --target "G:\Programming\OSBB_cl" `
    --db-access "C:\Users\first\Downloads\db_access.py" `
    --triage-script "G:\Programming\Py\OSBB_util\Scripts\osbb_cleanup_triage.py" `
    --dedupe-script "G:\Programming\Py\OSBB_util\Scripts\dedupe_shadowed_functions.py" `
    --harvest-script "G:\Programming\Py\OSBB\tools\harvest_lost_features_from_sandboxes.py" `
    --promote-script "G:\Programming\Py\OSBB\tools\promote_sandbox_to_training_db.py" `
    --dump-script "G:\Programming\Py\OSBB\tools\dump_service_codes_live_sandbox.py"