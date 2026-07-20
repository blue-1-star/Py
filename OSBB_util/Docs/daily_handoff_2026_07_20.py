#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSBB daily handoff installer for 2026-07-20.

Run from:
    G:\Programming\Py

Commands:
    python .\OSBB_util\Scripts\daily_handoff_2026_07_20.py --dry-run
    python .\OSBB_util\Scripts\daily_handoff_2026_07_20.py

The script is idempotent:
- creates a detailed daily handoff;
- adds a Chronicle entry;
- updates Current_Work;
- adds a concise Project Log entry;
- preserves all text outside managed blocks.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DATE = "2026-07-20"
MONTH = "2026-07"
PROJECT_DIR_NAME = "OSBB"
BEGIN = "<!-- BEGIN: OSBB-DAILY-2026-07-20 -->"
END = "<!-- END: OSBB-DAILY-2026-07-20 -->"

DAILY_HANDOFF = r'''
# DAILY HANDOFF

**Дата:** 20.07.2026

## Активная подсистема

**Subsystem:** Presentation Layer (UI)

Сегодня продолжилось развитие подсистемы представлений проекта OSBB.

Работы велись вокруг пользовательского интерфейса Telegram-кассира.

Основные рабочие модули:

```text
tools/cashier_v2_telegram/cashier_v2_ui.py
tools/cashier_v2_telegram/cashier_card.py
```

Именно эти модули формируют пользовательский опыт кассира и являются
первой точкой контакта человека с системой.

## Исходная практическая задача

Главным приоритетом проекта оставался запуск Telegram-кассы
в пилотную эксплуатацию.

Требовалось не абстрактное улучшение интерфейса, а подготовка кассы
к ежедневной работе с реальными платежами и реальными операторами.

За последние дни были реализованы либо обсуждались:

- сокращение количества экранов;
- уменьшение объема служебных сообщений;
- компактное отображение последних чеков;
- показ квартиры и автомобиля в одной строке;
- работа с несколькими автомобилями одной квартиры;
- автоматический выбор всех автомобилей по умолчанию;
- возможность частичной оплаты;
- подготовка временной схемы банковских платежей;
- мелкие исправления, выявленные во время реальной эксплуатации.

Каждое изменение возникало как реакция на конкретную ситуацию
в работе кассира, а не ради абстрактного совершенствования интерфейса.

## Возникшая инженерная проблема

Изменения перестали быть локальными.

Практически каждая новая идея требовала повторного вмешательства
в несколько частей Presentation Layer.

Перед очередным исправлением приходилось:

- искать предыдущие патчи;
- восстанавливать историю изменений;
- анализировать diff;
- проверять состояние Git;
- контролировать резервные копии;
- отслеживать версии файлов;
- вручную переносить накопленные изменения.

В результате значительная часть времени стала уходить не на развитие OSBB,
а на обслуживание самого процесса разработки.

Дальнейшее развитие интерфейса начало замедляться независимо
от сложности бизнес-задач.

## Принятое решение

Для устранения этого узкого места принято решение временно переключиться
на создание инженерного инструмента Assistant.

Assistant не является отдельной целью проекта.

Его назначение — вернуть разработчику возможность быстрее и безопаснее
развивать OSBB, не тратя основное время на ручное обслуживание патчей,
версий, резервных копий и диагностики.

## Новая подсистема

**Subsystem:** Development Infrastructure

Назначение подсистемы:

- применение патчей;
- диагностика проекта;
- контроль изменений;
- diff;
- резервное копирование;
- журналирование;
- сервисные операции разработчика.

Архитектура Assistant принята модульной.

## Влияние на архитектуру OSBB

К этому моменту в проекте последовательно формируются самостоятельные
подсистемы со своей ответственностью:

- **Core_New** — новый слой доступа к данным;
- **Finance_Core** — финансовое ядро;
- **Presentation Layer** — пользовательские представления;
- **Development Infrastructure** — инженерная инфраструктура разработки.

Каждая из этих подсистем появилась как ответ на конкретные практические
ограничения, обнаруженные во время развития проекта.

Архитектура OSBB развивается не хаотично и не по заранее нарисованной схеме,
а через последовательное выделение зон ответственности под давлением
реальных задач эксплуатации и разработки.

## Что изменилось за день

- Зафиксирована причина временного ухода от доработки кассира.
- Assistant определен как инфраструктурная подсистема OSBB.
- Принята модульная модель развития Assistant.
- Сформулирована связь между Presentation Layer и Development Infrastructure.
- Подтверждено, что главный приоритет проекта не изменился.

## Что осталось главным препятствием

Assistant еще не достиг минимально работоспособного состояния.

Пока это не произошло, доставка изменений в кассир остается дорогой
по времени и требует слишком большого количества ручных действий.

## Следующий шаг

После появления минимально работоспособной версии Assistant
разработка возвращается к Presentation Layer.

Главный приоритет:

> завершение Telegram-кассира и запуск кассы в пилотную эксплуатацию.
'''

CHRONICLE = r'''
## 2026-07-20 — Presentation Layer привел к появлению Development Infrastructure

### Откуда возникла задача

Основной практической целью проекта оставался запуск Telegram-кассы
в пилотную эксплуатацию.

Работы велись в модулях:

```text
tools/cashier_v2_telegram/cashier_v2_ui.py
tools/cashier_v2_telegram/cashier_card.py
```

Именно в них последовательно решались задачи сокращения экранов,
упрощения сообщений, компактного показа чеков, работы с несколькими
автомобилями, частичной оплаты и временной поддержки банковских платежей.

Все эти требования появились из реальных сценариев работы кассира.

### Почему проект временно изменил направление

Каждое новое изменение интерфейса стало требовать все больше
вспомогательной работы:

- поиска старых патчей;
- анализа diff;
- проверки Git;
- контроля резервных копий;
- отслеживания версий файлов;
- ручного переноса изменений.

Разработчик начал тратить больше времени на обслуживание процесса,
чем на развитие самого OSBB.

### Принятое решение

Развитие Presentation Layer временно приостановлено ради создания
минимально работоспособного Assistant.

Assistant определен не как самостоятельная цель, а как инфраструктурная
подсистема, которая должна ускорить и обезопасить развитие всех остальных
подсистем OSBB.

### Архитектурный результат

В проекте выделена новая подсистема:

**Development Infrastructure**

Ее зона ответственности:

- диагностика;
- применение патчей;
- diff;
- резервное копирование;
- журналирование;
- контроль состояния проекта;
- сервисные операции разработчика.

На этом этапе структура крупных подсистем OSBB выглядит так:

- Core_New;
- Finance_Core;
- Presentation Layer;
- Development Infrastructure.

Каждая подсистема возникла из конкретной практической необходимости,
а не из стремления заранее построить сложную архитектуру.

### Состояние на конец дня

Главный приоритет проекта не изменился:

> завершить Telegram-кассира и запустить кассу в пилотную эксплуатацию.

Работа над Assistant является временным инфраструктурным этапом,
необходимым для возвращения к этой задаче с более надежным
процессом разработки.
'''

CURRENT_WORK = r'''
# Current Work

## P0 — Запуск Telegram-кассы

**Подсистема:** Presentation Layer  
**Статус:** временно приостановлено ради устранения инфраструктурного узкого места.

### Почему задача приоритетна

Касса нужна для реальной работы, приема платежей и ввода текущих данных.

### Рабочие модули

```text
tools/cashier_v2_telegram/cashier_v2_ui.py
tools/cashier_v2_telegram/cashier_card.py
```

### Уже сформированные требования

- компактный интерфейс;
- сокращение служебных сообщений;
- короткое отображение последних чеков;
- квартира и автомобиль в одной строке;
- несколько автомобилей квартиры;
- выбор всех автомобилей по умолчанию;
- частичная оплата;
- временная поддержка банковского платежа.

### Текущее препятствие

Изменения слишком дороги по времени из-за ручной работы с патчами,
diff, Git, резервными копиями и версиями файлов.

### Следующий шаг

Вернуться к Presentation Layer сразу после появления
минимально работоспособного Assistant.

---

## P0 — Минимально работоспособный Assistant

**Подсистема:** Development Infrastructure  
**Статус:** в работе.

### Почему задача появилась

Она возникла непосредственно из проблем развития Telegram-кассира.

Assistant нужен не сам по себе, а для устранения потерь времени
при доставке и проверке изменений Presentation Layer.

### Минимальная зона ответственности

- определение project root и Git root;
- проверка обязательных файлов;
- diff;
- резервное копирование;
- применение изменений;
- проверка результата;
- понятная диагностика ошибок.

### Критерий завершения этапа

Разработчик может безопасно получить, проверить и применить изменение
без ручного поиска файлов, версий и предыдущих патчей.

### После завершения

Немедленный возврат к Telegram-кассиру.
'''

PROJECT_LOG = r'''
## 2026-07-20 — Presentation Layer и начало Development Infrastructure

Продолжалась подготовка Telegram-кассира к пилотной эксплуатации.

Работы концентрировались в:

```text
tools/cashier_v2_telegram/cashier_v2_ui.py
tools/cashier_v2_telegram/cashier_card.py
```

На фоне последовательных UI-доработок обнаружено инфраструктурное
узкое место: слишком много времени уходило на патчи, diff, Git,
резервные копии и перенос версий файлов.

Принято решение временно переключиться на минимальную версию Assistant.

Assistant определен как новая подсистема **Development Infrastructure**,
обслуживающая развитие Core_New, Finance_Core, Presentation Layer
и других частей OSBB.

Главный приоритет не изменен: после стабилизации Assistant работа
возвращается к завершению Telegram-кассира.
'''


def managed_block(content: str) -> str:
    return f"{BEGIN}\n{content.strip()}\n{END}\n"


def detect_project_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"Project root does not exist: {root}")
        return root

    cwd = Path.cwd().resolve()
    if cwd.name.lower() == PROJECT_DIR_NAME.lower():
        return cwd

    candidate = cwd / PROJECT_DIR_NAME
    if candidate.exists():
        return candidate.resolve()

    raise FileNotFoundError(
        "OSBB project root was not found.\n"
        "Run from G:\\Programming\\Py or use --project-root."
    )


def upsert(path: Path, content: str, dry_run: bool) -> str:
    block = managed_block(content)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    if BEGIN in existing and END in existing:
        start = existing.index(BEGIN)
        end = existing.index(END) + len(END)
        new_text = existing[:start] + block.rstrip() + existing[end:]
        new_text = new_text.rstrip() + "\n"
        action = "unchanged" if new_text == existing else "updated"
    else:
        prefix = existing.rstrip()
        if prefix:
            prefix += "\n\n"
        new_text = prefix + block
        action = "created" if not existing else "updated"

    if not dry_run and new_text != existing:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_text, encoding="utf-8", newline="\n")

    return action


def pick_existing(project_root: Path, candidates: list[str]) -> Path:
    paths = [project_root / candidate for candidate in candidates]
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install OSBB daily handoff and Chronicle entry for 2026-07-20."
    )
    parser.add_argument("--project-root", help="Explicit path to the OSBB project root.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without writing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        project_root = detect_project_root(args.project_root)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    docs = project_root / "Docs"
    targets = [
        (docs / "Daily" / f"{DATE}.md", DAILY_HANDOFF, "Detailed daily handoff"),
        (docs / "Chronicle" / f"{MONTH}.md", CHRONICLE, "Project Chronicle"),
        (
            pick_existing(project_root, ["Docs/Current_Work.md", "Docs/CURRENT_WORK.md", "Current_Work.md"]),
            CURRENT_WORK,
            "Current priorities",
        ),
        (
            pick_existing(project_root, ["Docs/Project_Log.md", "Docs/PROJECT_LOG.md", "Project_Log.md"]),
            PROJECT_LOG,
            "Project log",
        ),
    ]

    print("=" * 72)
    print("OSBB Daily Handoff installer")
    print("=" * 72)
    print(f"Project root: {project_root}")
    print(f"Mode        : {'DRY-RUN' if args.dry_run else 'APPLY'}")
    print()

    changed = 0
    for path, content, label in targets:
        action = upsert(path, content, args.dry_run)
        if action != "unchanged":
            changed += 1
        print(f"[{action.upper():9}] {path.relative_to(project_root)}")
        print(f"             {label}")

    print()
    print(f"Changed files: {changed}")

    if args.dry_run:
        print("No files were written.")
        return 0

    errors: list[str] = []
    for path, _, _ in targets:
        if not path.exists():
            errors.append(f"Missing: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            errors.append(f"Managed block not found: {path}")

    if errors:
        print()
        print("[VERIFY FAILED]")
        for error in errors:
            print(f"- {error}")
        return 3

    print()
    print("[VERIFY OK]")
    print("Daily handoff, Chronicle, Current Work and Project Log were updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
