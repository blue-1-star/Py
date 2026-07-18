#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI-018 v3 — устойчивый к форматированию патчер.

Запуск из корня G:\Programming\Py:
    python UI-018_apply_v3.py --check
    python UI-018_apply_v3.py
    python UI-018_apply_v3.py --revert
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REL_CARD = Path("OSBB/tools/cashier_v2_telegram/cashier_card.py")
REL_UI = Path("OSBB/tools/cashier_v2_telegram/cashier_v2_ui.py")
SUFFIX = ".bak.UI-018-v3"


def root_from(start: Path) -> Path:
    for root in (start.resolve(), *start.resolve().parents):
        if (root / REL_CARD).is_file() and (root / REL_UI).is_file():
            return root
    raise FileNotFoundError("Не найден корень репозитория G:\\Programming\\Py.")


def regex_once(text: str, pattern: str, repl: str, label: str) -> str:
    result, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: найдено совпадений {count}, ожидалось 1.")
    return result


def literal_all(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        raise RuntimeError(f"{label}: фрагмент не найден.")
    return text.replace(old, new)


def build(root: Path) -> dict[Path, str]:
    card_path = root / REL_CARD
    ui_path = root / REL_UI
    card = card_path.read_text(encoding="utf-8")
    ui = ui_path.read_text(encoding="utf-8")

    # Удаляем пустой элемент сразу после payer_title(payer), независимо от пробелов/переносов.
    card = regex_once(
        card,
        r"(lines\s*=\s*\[\s*payer_title\(payer\)\s*,)\s*(['\"]{2})\s*,",
        r"\1",
        "cashier_card/header-empty-line",
    )

    # Удаляем пустой элемент в начале блока lines.extend перед строкой «Услуга».
    card = regex_once(
        card,
        r"(lines\.extend\(\s*\[\s*)['\"]{2}\s*,\s*(f?['\"]Услуга:)",
        r"\1\2",
        "cashier_card/service-empty-line",
    )

    # Удаляем пустой элемент между комментарием и подтверждением.
    card = regex_once(
        card,
        r"(f?['\"]Комментарий:\s*\{comment\}['\"]\s*,)\s*['\"]{2}\s*,\s*(['\"]Если всё верно)",
        r"\1 \2",
        "cashier_card/confirm-empty-line",
    )

    replacements = [
        (
            " Касса v0.4.4\n\nВыберите группу субъекта расчётов.",
            " Касса v0.4.4\nВыберите группу субъекта расчётов.",
            "ui/start",
        ),
        (
            " Найдите плательщика\n\nВведите номер квартиры или несколько цифр госномера автомобиля.\n\nНапример: 98 или 3804.",
            " Найдите плательщика\nВведите номер квартиры или несколько цифр госномера автомобиля.\nНапример: 98 или 3804.",
            "ui/payer-search",
        ),
        (
            " Другая услуга\n\nВыберите группу:",
            " Другая услуга\nВыберите группу:",
            "ui/other-service",
        ),
        (
            " Коммерческие фирмы\n\nВведите часть названия, номер помещения или номер договора.",
            " Коммерческие фирмы\nВведите часть названия, номер помещения или номер договора.",
            "ui/commercial-search",
        ),
        (
            " Жильцы / Авто\n\nВведите номер квартиры или несколько цифр госномера автомобиля.",
            " Жильцы / Авто\nВведите номер квартиры или несколько цифр госномера автомобиля.",
            "ui/resident-search",
        ),
        (
            " Ввод данных авто\n\nНомер/фрагмент: {fragment}\n\nВведите квартиру, если она известна, или нажмите «Пропустить квартиру».",
            " Ввод данных авто\nНомер/фрагмент: {fragment}\nВведите квартиру, если она известна, или нажмите «Пропустить квартиру».",
            "ui/vehicle-entry",
        ),
        (
            "⚠ Автомобиль или квартира не найдены.\n\nИзвестный номер/фрагмент: {text}\n\nМожно сразу ввести данные авто.",
            "⚠ Автомобиль или квартира не найдены.\nИзвестный номер/фрагмент: {text}\nМожно сразу ввести данные авто.",
            "ui/not-found",
        ),
        (
            " Другое\n\nВыберите группу:",
            " Другое\nВыберите группу:",
            "ui/misc",
        ),
    ]

    for old, new, label in replacements:
        ui = literal_all(ui, old, new, label)

    return {card_path: card, ui_path: ui}


def backup(path: Path) -> Path:
    return path.with_name(path.name + SUFFIX)


def check(root: Path) -> None:
    changes = build(root)
    print("UI-018 v3: проверка пройдена.")
    for path in changes:
        print(f"  готов: {path.relative_to(root)}")


def apply(root: Path) -> None:
    changes = build(root)
    for path in changes:
        if backup(path).exists():
            raise FileExistsError(f"Уже существует backup: {backup(path)}")
    for path, content in changes.items():
        shutil.copy2(path, backup(path))
        path.write_text(content, encoding="utf-8", newline="")
        print(f"изменён: {path.relative_to(root)}")
    print("Готово. Теперь выполните: git diff --check")


def revert(root: Path) -> None:
    restored = 0
    for rel in (REL_CARD, REL_UI):
        path = root / rel
        bak = backup(path)
        if bak.exists():
            shutil.copy2(bak, path)
            bak.unlink()
            restored += 1
            print(f"восстановлен: {path.relative_to(root)}")
    if not restored:
        raise FileNotFoundError("Backup UI-018 v3 не найден.")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--revert", action="store_true")
    args = parser.parse_args()

    try:
        root = root_from(Path.cwd())
        if args.revert:
            revert(root)
        elif args.check:
            check(root)
        else:
            apply(root)
        return 0
    except Exception as exc:
        print(f"UI-018 v3 ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
