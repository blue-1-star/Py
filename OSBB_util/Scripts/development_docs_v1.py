#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Idempotent installer for OSBB Development Docs v1."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from dataclasses import dataclass
from pathlib import Path

PACKAGE = "Development Docs v1"
VERSION = "1.0.0"
BEGIN = "<!-- BEGIN: DEVELOPMENT-DOCS-V1 -->"
END = "<!-- END: DEVELOPMENT-DOCS-V1 -->"


@dataclass(frozen=True)
class Doc:
    path: str
    body: str


def block(body: str) -> str:
    return f"{BEGIN}\n{body.strip()}\n{END}\n"


def upsert(existing: str, managed: str) -> tuple[str, str]:
    if BEGIN in existing and END in existing:
        start = existing.index(BEGIN)
        finish = existing.index(END) + len(END)
        new = (existing[:start] + managed.rstrip() + existing[finish:]).rstrip() + "\n"
        return new, "unchanged" if new == existing else "updated"
    prefix = existing.rstrip()
    if prefix:
        prefix += "\n\n"
    return prefix + managed, "created" if not existing else "updated"


def detect_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(root)
        return root
    cwd = Path.cwd().resolve()
    if (cwd / "OSBB").is_dir():
        return (cwd / "OSBB").resolve()
    if cwd.name.lower() == "osbb":
        return cwd
    raise FileNotFoundError(
        "OSBB project root was not found. Run from G:\\Programming\\Py "
        "or use --project-root."
    )


def docs() -> list[Doc]:
    return [
        Doc("Docs/Development/README.md", r'''# Development Documentation

## Назначение

Раздел `Docs/Development` хранит инженерные знания проекта OSBB: принципы,
ошибки, способы диагностики, особенности окружения и развитие внутренних
инструментов.

## Состав

- `Engineering_Principles.md`
- `Assistant_Development.md`
- `Lessons_Learned.md`
- `Troubleshooting.md`
- `Environment.md`
- `Presentation_Layer.md`
- `Query_Library.md`

## Основной принцип

Любая проблема, на решение которой ушло значительное время, должна оставить
после себя документ, тест, автоматическую проверку или новую функцию Assistant.

Пакет: **Development Docs v1**  
Версия: **1.0.0**
'''),
        Doc("Docs/Development/Engineering_Principles.md", r'''# Engineering Principles

## 1. Каждый найденный ключ должен получить свой крючок

Решение не должно оставаться только в памяти разработчика или в истории чата.
Оно должно превратиться в документ, тест, проверку или функцию Assistant.

## 2. Проверка важнее предположения

Сначала факты о текущем состоянии системы, потом изменение.

## 3. Проверка перед действием

```text
check
  ↓
dry-run
  ↓
apply / install
  ↓
verify
```

## 4. Ошибка должна становиться проверкой

Каждый повторяемый класс ошибок должен постепенно превращаться в диагностику.

## 5. Повторяющееся действие должно быть автоматизировано

Если операция повторяется, она должна стать командой Assistant либо модулем.

## 6. Документация является частью результата

Код без необходимой документации считается незавершенным.

## 7. Сначала сохранить состояние, затем изменять

Перед опасной операцией нужны diff, резервная точка, способ отмены и проверка.

## 8. Не искать иголку вручную

Assistant должен сам сообщать пути, найденные файлы, отсутствующие файлы,
выполняемую команду и причину остановки.

## 9. Правило Lessons Learned

Если проблема отняла более 30–60 минут, нужно:

1. добавить запись в `Lessons_Learned.md`;
2. обновить `Troubleshooting.md`;
3. определить новую автоматическую проверку;
4. зафиксировать технический долг.
'''),
        Doc("Docs/Development/Assistant_Development.md", r'''# Assistant Development

## Назначение

Assistant должен стать единым инженерным интерфейсом проекта OSBB, а не
набором разрозненных скриптов.

## Цели

Assistant постепенно объединяет:

- Environment Detector;
- Project Doctor;
- Document Installer;
- Patch Engine;
- Diff Analyzer;
- Backup Engine;
- Query Engine;
- Verification Engine;
- журнал инженерного опыта.

## Базовый принцип

Assistant должен объяснять, что обнаружено, что будет изменено, почему это
безопасно, что изменилось и как проверить или отменить результат.

## Этапы

### 0.x — прототипы

Отдельные сервисные скрипты, первые проверки окружения, установка документации,
патчи и проверка файлов.

### 1.x — единая консоль

```text
assistant doctor
assistant env
assistant where
assistant check
assistant diff
assistant backup
assistant apply
assistant verify
assistant log
```

### 2.x — Query Engine

```text
assistant query list
assistant query show <name>
assistant query run <name>
```

### 3.x — сопровождение документации

```text
assistant docs check
assistant docs install
assistant docs verify
assistant docs lesson
assistant docs roadmap
assistant docs adr
```

## Обязательные свойства

- идемпотентность;
- dry-run;
- проверяемость;
- понятная диагностика;
- обратимость опасных изменений.

## Ближайший технический долг

- стабилизировать поиск project root и Git root;
- стандартизировать Windows-пути;
- добавить `doctor`, `env`, `where`, `verify`;
- исключить ручной поиск файлов пользователем.
'''),
        Doc("Docs/Development/Lessons_Learned.md", r'''# Lessons Learned

## 2026-07-20 — попытки поднять Assistant

### Контекст

В течение рабочего дня предпринимались последовательные попытки запустить и
стабилизировать Assistant. Каждая гипотеза требовала ручного поиска и проверки.

### Проблема

Пользователь был вынужден вручную выполнять работу диагностического инструмента
и искать «иголку в стоге сена».

### Причины

- отсутствовала единая команда диагностики;
- гипотезы проверялись вручную;
- не было надежного определения project root и Git root;
- ожидания скрипта не совпадали с реальной структурой;
- сообщения об ошибках не давали полного ответа;
- найденные причины не превращались сразу в постоянные проверки.

### Главный вывод

Пользователь не должен угадывать, где находится ошибка. Assistant обязан сам
собрать факты и выдать диагностический отчет.

### Необходимые команды

```text
assistant doctor
assistant env
assistant where
assistant check
assistant verify
```

### Обязательная последовательность

```text
check
  ↓
dry-run
  ↓
apply
  ↓
verify
```

### Что автоматизировать

- поиск корня проекта и Git root;
- проверку обязательных файлов;
- проверку Python и кодировки;
- проверку структуры `Docs` и путей к `OSBB_util`;
- вывод точной команды запуска;
- подтверждение результата после операции.

### Организационный вывод

Каждая дорогая по времени ошибка должна завершаться записью в документации,
обновлением troubleshooting и новой проверкой либо задачей в Roadmap.
'''),
        Doc("Docs/Development/Troubleshooting.md", r'''# Troubleshooting

## Шаблон записи

```text
## Название проблемы
### Симптомы
### Причина
### Диагностика
### Решение
### Предотвращение
```

## Assistant не запускается из ожидаемого каталога

### Симптомы

Python не находит файл, относительные пути ведут не туда, пользователь вручную
ищет нужный файл.

### Возможные причины

- команда запущена не из `G:\Programming\Py`;
- смешаны project root и Git root;
- используется жестко заданный путь;
- команда написана для `cmd.exe`, а запускается в PowerShell.

### Диагностика

```powershell
Get-Location
Test-Path .\OSBB
Test-Path .\OSBB_util
Get-ChildItem .\OSBB_util\Scripts
git rev-parse --show-toplevel
python --version
```

### Решение

Запускать из `G:\Programming\Py`, выводить обнаруженные пути и при необходимости
передавать `--project-root`.

### Предотвращение

Добавить `assistant where`, `assistant env`, `assistant doctor`.

## Документатор не находит Docs

### Решение

```powershell
python .\OSBB_util\Scripts\development_docs_v1.py `
  --project-root .\OSBB
```

## Повторный запуск дублирует документацию

Установщик должен использовать управляемые маркеры и заменять только содержимое
между ними, сохраняя ручной текст вне блока.
'''),
        Doc("Docs/Development/Environment.md", r'''# Development Environment

## Рабочая система

- Windows
- Visual Studio Code
- PowerShell

## Рабочий каталог

```text
G:\Programming\Py
```

## Структура

```text
G:\Programming\Py\
├── .git\
├── OSBB\
│   └── Docs\
└── OSBB_util\
    ├── Scripts\
    └── Patches\
```

## Project root

```text
G:\Programming\Py\OSBB
```

## Git root

```text
G:\Programming\Py
```

Project root и Git root — разные каталоги.

## Соглашения

Команды пишутся для PowerShell. Использовать `$env:USERPROFILE`, а не
`%USERPROFILE%`.

Предпочтительный запуск:

```powershell
python .\OSBB_util\Scripts\<script_name>.py
```

Перед операцией Assistant должен вывести текущий каталог, Git root, project
root, Python, обязательные файлы и каталог назначения.
'''),
        Doc("Docs/Development/Presentation_Layer.md", r'''# Presentation Layer

## Назначение

Presentation Layer преобразует состояние системы в понятное представление для
пользователя и не содержит бизнес-логику.

```text
Business Logic
      ↓
State / Result
      ↓
Presentation Layer
      ↓
Telegram / Web / Desktop / Assistant
```

## UI-020

После успешной операции пользователь получает не абстрактное сообщение об
успехе, а актуальное состояние кассы или другого затронутого объекта.

Первый объект:

```python
render_cashier_state(...)
```

Планируемое семейство:

```python
render_cashier_state(...)
render_apartment_state(...)
render_vehicle_state(...)
render_resident_state(...)
render_service_state(...)
render_payment_state(...)
render_finance_state(...)
```

## Принципы

- бизнес-логика возвращает состояние, а не Telegram-текст;
- форматирование отделено от изменения данных;
- один объект состояния отображается в разных клиентах;
- Telegram — первый клиент, но не центр архитектуры.
'''),
        Doc("Docs/Development/Query_Library.md", r'''# Query Library

## Назначение

Query Library — библиотека именованных диагностических SQL-запросов для
просмотра сложных связей в нормализованной базе OSBB.

## Цели

- объединять данные из нескольких таблиц;
- показывать неочевидные связи;
- ускорять диагностику;
- предоставлять повторно используемые отчеты.

## Безопасность

Все запросы по умолчанию только для чтения. Базовый разрешенный класс:

```sql
SELECT ...
```

## Категории

- View;
- Control;
- Analytics;
- Finance;
- Audit.

## Примеры имен

```text
parking.multiple_cars
parking.unknown_vehicle_fragments
finance.debtors
finance.payments_by_period
audit.deleted_today
apartments.without_residents
```

## Будущий объект запроса

- уникальное имя;
- описание;
- категория;
- SQL;
- параметры;
- ожидаемые колонки;
- уровень доступа;
- `read_only`;
- примеры использования.

## Интеграция с Assistant

```text
assistant query list
assistant query show parking.multiple_cars
assistant query run parking.multiple_cars
assistant query run finance.debtors --param period=2026-07
```

## Эволюция

```text
Loose SQL files
      ↓
Query Library
      ↓
Named Query Objects
      ↓
Query Engine
      ↓
Assistant / UI / Reports
```
'''),
    ]


def choose(root: Path, names: list[str]) -> Path:
    for name in names:
        p = root / name
        if p.exists():
            return p
    return root / names[0]


def write_managed(path: Path, body: str, dry_run: bool) -> str:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    new, action = upsert(existing, block(body))
    if not dry_run and new != existing:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8", newline="\n")
    return action


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Install OSBB Development Docs v1")
    p.add_argument("--project-root")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-roadmap", action="store_true")
    p.add_argument("--no-project-log", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = detect_root(args.project_root)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    print("=" * 72)
    print(f"{PACKAGE} installer v{VERSION}")
    print("=" * 72)
    print(f"Current dir : {Path.cwd()}")
    print(f"Project root: {root}")
    print(f"Mode        : {'DRY-RUN' if args.dry_run else 'APPLY'}")
    print()

    changed = 0
    planned = docs()
    for doc in planned:
        action = write_managed(root / doc.path, doc.body, args.dry_run)
        changed += action != "unchanged"
        print(f"[{action.upper():9}] {doc.path}")

    if not args.no_roadmap:
        roadmap = choose(root, ["Docs/ROADMAP.md", "Docs/Roadmap.md", "ROADMAP.md"])
        roadmap_body = r'''## Development Docs v1

- [x] Создать `Docs/Development`.
- [x] Зафиксировать инженерные принципы.
- [x] Создать Lessons Learned и Troubleshooting.
- [x] Зафиксировать окружение.
- [x] Описать Presentation Layer и Query Library.
- [ ] Реализовать `assistant doctor`.
- [ ] Реализовать `assistant env`.
- [ ] Реализовать `assistant where`.
- [ ] Реализовать `assistant verify`.
- [ ] Научить Assistant сопровождать инженерную документацию.
'''
        action = write_managed(roadmap, roadmap_body, args.dry_run)
        changed += action != "unchanged"
        print(f"[{action.upper():9}] {roadmap.relative_to(root)}")

    if not args.no_project_log:
        log = choose(root, ["Docs/Project_Log.md", "Docs/PROJECT_LOG.md", "Project_Log.md"])
        today = dt.date.today().isoformat()
        log_body = f'''## {today} — Development Docs v1

Создан пакет инженерной документации `Docs/Development`.

Зафиксированы выводы из неудачных попыток запуска Assistant: ручной поиск причин
должен быть заменен встроенной диагностикой.

Принят принцип: каждая дорогая по времени ошибка должна превращаться в документ,
проверку, тест или функцию Assistant.
'''
        action = write_managed(log, log_body, args.dry_run)
        changed += action != "unchanged"
        print(f"[{action.upper():9}] {log.relative_to(root)}")

    print()
    print(f"Changed files: {changed}")
    if args.dry_run:
        print("Dry-run completed. No files were written.")
        return 0

    missing = [d.path for d in planned if not (root / d.path).exists()]
    if missing:
        print("[VERIFY FAILED]", file=sys.stderr)
        for item in missing:
            print(f"- Missing: {item}", file=sys.stderr)
        return 3

    print("[VERIFY OK] Development Docs v1 installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
