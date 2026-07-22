#!/usr/bin/env python3
"""
init_osbb_cl_skeleton.py
==========================

Материализует пустой каркас проекта OSBB_cl на диске — согласованную
структуру папок, config.py, .gitignore, README-заглушку — и по желанию
инициализирует git.

Ничего не удаляет и не трогает старый OSBB. Если целевая папка уже
существует и не пуста — скрипт остановится и попросит --force, чтобы
не затереть что-то по ошибке.

Как запускать:

    python init_osbb_cl_skeleton.py --root "G:\\Programming\\OSBB_cl"

Это создаст:

    OSBB_cl/
    ├── .gitignore
    ├── config.py
    ├── README.md
    ├── requirements.txt
    ├── core_new/
    │   ├── __init__.py
    │   ├── adapters/__init__.py
    │   └── domain/__init__.py
    ├── finance_core/
    │   └── __init__.py
    ├── presentation/
    │   ├── handlers/.gitkeep
    │   └── cashier_v2_telegram/.gitkeep
    ├── dev_infrastructure/.gitkeep
    ├── data/
    │   ├── db/.gitkeep
    │   ├── raw/typed/.gitkeep
    │   ├── logs/.gitkeep
    │   ├── exports/.gitkeep
    │   └── reports/.gitkeep
    ├── migrations/.gitkeep
    └── docs/.gitkeep

С флагом --git-init дополнительно выполнит `git init` и первый коммит
("initial skeleton") — независимый репозиторий, без связи с историей Py/.
"""

import argparse
import subprocess
import sys
from pathlib import Path


CONFIG_PY_CONTENT = '''# config.py (в корне OSBB_cl/)
#
# Кроссплатформенный конфиг путей, выделенный только под OSBB_cl.
# Структура ЗЕРКАЛЬНА старому OSBB (Bots/, tools/, core_new/, Data/, Docs/) —
# осознанное решение: минимум риска сломать импорты при переносе.
# Реорганизация по подсистемам (presentation/, business_core/ и т.п.) —
# отдельная, постепенная задача на потом, когда всё уже работает.

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
        # ДАННЫЕ — имена папок зеркальны старому OSBB
        # ==================================================
        self.DATA_DIR = self.PROJECT_ROOT / "Data"
        self.RAW_DIR = self.DATA_DIR / "raw"
        self.TYPED_DIR = self.RAW_DIR / "typed"
        self.DB_DIR = self.DATA_DIR / "db"
        self.EXPORTS_DIR = self.DATA_DIR / "exports"
        self.LOGS_DIR = self.DATA_DIR / "logs"
        self.BACKUPS_DIR = self.DB_DIR / "backups"

        self.DB_FILE = self.DB_DIR / "osbb_test.db"  # это и есть боевая база, несмотря на имя — переименовывать не будем, только путаница

        # ==================================================
        # СОВМЕСТИМОСТЬ СО СТАРЫМ ИНТЕРФЕЙСОМ config.py
        # ==================================================
        # Старый код (ещё не адаптированный) ожидает paths.OSBB_TEST_DB_FILE /
        # paths.OSBB_DB_FILE и глобальную USE_TEST_DB. В OSBB_cl база одна —
        # но вместо правки каждого файла-потребителя (десятки мест) даём
        # мягкие алиасы на ту же самую БД. Тот же принцип, что и db_adapter.py:
        # не переписывать вызывающих, а подставить совместимую прослойку.
        self.OSBB_TEST_DB_FILE = self.DB_FILE
        self.OSBB_DB_FILE = self.DB_FILE

        # ==================================================
        # ДОКУМЕНТАЦИЯ
        # ==================================================
        self.DOCS_DIR = self.PROJECT_ROOT / "Docs"

    def ensure_directories(self):
        """Создаёт недостающие рабочие папки (не трогает git/секреты)."""
        dirs = [
            self.DATA_DIR,
            self.RAW_DIR,
            self.TYPED_DIR,
            self.DB_DIR,
            self.EXPORTS_DIR,
            self.LOGS_DIR,
            self.DOCS_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)


# ✅ ЕДИНЫЙ ЭКЗЕМПЛЯР — как и в старом config.py
paths = ProjectPaths()

# Совместимость: старый код делает "from config import paths, USE_TEST_DB".
# В OSBB_cl база одна (paths.DB_FILE), но само имя оставляем существующим,
# чтобы не редактировать каждого потребителя. Значение не влияет на то,
# какая БД используется — она одна и та же в любом случае.
USE_TEST_DB = True
'''

GITIGNORE_CONTENT = '''__pycache__/
*.pyc
.venv/
venv/
*.diff
*.log

# отчёты dev_infrastructure — генерируются заново, не храним в истории
osbb_triage_report.*
'''

README_CONTENT = '''# OSBB_cl

Чистый каркас проекта OSBB, начатый заново — отдельный git,
отдельный config.py, только то, что реально служит цели: довести
Telegram-кассира до пилотной эксплуатации.

Структура ЗЕРКАЛЬНА старому OSBB (Bots/, tools/, core_new/, Data/, Docs/,
*_core.py в корне) — осознанное решение в пользу нулевого риска сломать
импорты при переносе. Реорганизация по смысловым подсистемам
(presentation/business_core/finance_core и т.п.) — отдельная, постепенная
задача на потом, по аналогии с тем, как в своё время внедряли core_new:
через мягкую прослойку-адаптер, а не одним разрушительным рывком.

Известные подсистемы (пока не физическая структура папок, а ориентир):
- Core_New (core_new/) — новый слой доступа к данным
- Finance_Core — финансовые правила (в т.ч. неразнесённые платежи) — пока не выделен
- Presentation (Bots/, tools/) — пользовательский интерфейс
- Development Infrastructure (dev_infrastructure/) — инструменты разработки
'''

REQUIREMENTS_CONTENT = '''# TODO: перенести реальный список зависимостей из старого OSBB
'''

# (относительный путь, is_package) — is_package=True создаёт __init__.py,
# False — создаёт .gitkeep, чтобы папка не потерялась в git при пустом виде
DIRS = [
    ("Bots", False),
    ("Bots/handlers", False),
    ("tools", False),
    ("tools/cashier_v2_telegram", False),
    ("tools/cashier_admin", False),
    ("tools/user_onboarding", False),
    ("core_new", True),
    ("core_new/adapters", True),
    ("core_new/domain", True),
    ("dev_infrastructure", False),
    ("Data/db", False),
    ("Data/raw/typed", False),
    ("Data/logs", False),
    ("Data/exports", False),
    ("migrations", False),
    ("Docs", False),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help=r'Куда положить OSBB_cl, например "G:\Programming\OSBB_cl"')
    ap.add_argument("--force", action="store_true", help="Продолжить, даже если папка --root уже существует и не пуста")
    ap.add_argument("--git-init", action="store_true", help="Выполнить git init и первый коммит после создания структуры")
    args = ap.parse_args()

    root = Path(args.root).resolve()

    if root.exists() and any(root.iterdir()) and not args.force:
        print(f"Папка уже существует и не пуста: {root}", file=sys.stderr)
        print("Если это ожидаемо (например, повторный запуск) — добавьте --force.", file=sys.stderr)
        sys.exit(1)

    root.mkdir(parents=True, exist_ok=True)
    print(f"Создаю каркас в: {root}")

    for rel, is_package in DIRS:
        d = root / rel
        d.mkdir(parents=True, exist_ok=True)
        if is_package:
            init_file = d / "__init__.py"
            if not init_file.exists():
                init_file.write_text("", encoding="utf-8")
        else:
            keep_file = d / ".gitkeep"
            if not keep_file.exists():
                keep_file.write_text("", encoding="utf-8")
        print(f"  {rel}/")

    files = {
        "config.py": CONFIG_PY_CONTENT,
        ".gitignore": GITIGNORE_CONTENT,
        "README.md": README_CONTENT,
        "requirements.txt": REQUIREMENTS_CONTENT,
    }
    for name, content in files.items():
        f = root / name
        if not f.exists() or args.force:
            f.write_text(content, encoding="utf-8")
            print(f"  {name}")

    print("\nСтруктура создана.")

    if args.git_init:
        git_dir = root / ".git"
        if git_dir.exists():
            print("git уже инициализирован здесь, пропускаю git init.")
        else:
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "initial skeleton: структура OSBB_cl"],
                cwd=root,
                check=True,
            )
            print("git инициализирован, сделан первый коммит.")

    print(f"\nГотово. Дальше можно копировать подтверждённые живые файлы в {root}")


if __name__ == "__main__":
    main()
