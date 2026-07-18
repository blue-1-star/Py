#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI-018 v4 — патчер для фактического однострочного исходника из commit
91b0f98852ea705051d00793e7f40e71a720f0dc.

Запуск из корня репозитория:
    python UI-018_apply_v4.py --check
    python UI-018_apply_v4.py
    python UI-018_apply_v4.py --revert
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REL_CARD = Path("OSBB/tools/cashier_v2_telegram/cashier_card.py")
REL_UI = Path("OSBB/tools/cashier_v2_telegram/cashier_v2_ui.py")
BACKUP_SUFFIX = ".bak.UI-018-v4"


def find_root(start: Path) -> Path:
    for root in (start.resolve(), *start.resolve().parents):
        if (root / REL_CARD).is_file() and (root / REL_UI).is_file():
            return root
    raise FileNotFoundError("Не найден корень репозитория с каталогом OSBB.")


def replace_exact(text: str, old: str, new: str, label: str, expected: int = 1) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(
            f"{label}: найдено вхождений {count}, ожидалось {expected}. "
            "Файлы не изменены."
        )
    return text.replace(old, new)


def build_changes(root: Path) -> dict[Path, str]:
    card_path = root / REL_CARD
    ui_path = root / REL_UI

    card = card_path.read_text(encoding="utf-8")
    ui = ui_path.read_text(encoding="utf-8")

    # cashier_card.py — убираем декоративные пустые строки карточки.
    card = replace_exact(
        card,
        "lines = [ payer_title(payer), '', f\"Квартира: {payer.get('apartment_number') or '—'}\", ]",
        "lines = [ payer_title(payer), f\"Квартира: {payer.get('apartment_number') or '—'}\", ]",
        "cashier_card/header",
    )
    card = replace_exact(
        card,
        "lines.extend([ '', f\"Услуга: {service_name}\"",
        "lines.extend([ f\"Услуга: {service_name}\"",
        "cashier_card/service",
    )
    card = replace_exact(
        card,
        "f\"Комментарий: {comment}\", '', 'Если всё верно — подтвердите.\\nИначе измените только нужное поле.'",
        "f\"Комментарий: {comment}\", 'Если всё верно — подтвердите.\\nИначе измените только нужное поле.'",
        "cashier_card/confirmation",
    )

    # В исходном Python-файле переводы строк внутри сообщений записаны
    # как два символа: обратная косая черта + n. Поэтому ищем именно \\n.
    replacements = [
        (
            '" Касса v0.4.4\\n\\nВыберите группу субъекта расчётов."',
            '" Касса v0.4.4\\nВыберите группу субъекта расчётов."',
            "ui/start",
            1,
        ),
        (
            '" Найдите плательщика\\n\\nВведите номер квартиры или несколько цифр госномера автомобиля.\\n\\nНапример: 98 или 3804."',
            '" Найдите плательщика\\nВведите номер квартиры или несколько цифр госномера автомобиля.\\nНапример: 98 или 3804."',
            "ui/payer-search",
            1,
        ),
        (
            '" Другая услуга\\n\\nВыберите группу:"',
            '" Другая услуга\\nВыберите группу:"',
            "ui/other-service",
            1,
        ),
        (
            '" Коммерческие фирмы\\n\\nВведите часть названия, номер помещения или номер договора."',
            '" Коммерческие фирмы\\nВведите часть названия, номер помещения или номер договора."',
            "ui/commercial-search",
            2,
        ),
        (
            '" Жильцы / Авто\\n\\nВведите номер квартиры или несколько цифр госномера автомобиля."',
            '" Жильцы / Авто\\nВведите номер квартиры или несколько цифр госномера автомобиля."',
            "ui/resident-search",
            3,
        ),
        (
            'f" Ввод данных авто\\n\\nНомер/фрагмент: {fragment}\\n\\nВведите квартиру, если она известна, или нажмите «Пропустить квартиру»."',
            'f" Ввод данных авто\\nНомер/фрагмент: {fragment}\\nВведите квартиру, если она известна, или нажмите «Пропустить квартиру»."',
            "ui/vehicle-entry",
            1,
        ),
        (
            'f"⚠ Автомобиль или квартира не найдены.\\n\\nИзвестный номер/фрагмент: {text}\\n\\nМожно сразу ввести данные авто."',
            'f"⚠ Автомобиль или квартира не найдены.\\nИзвестный номер/фрагмент: {text}\\nМожно сразу ввести данные авто."',
            "ui/not-found",
            1,
        ),
        (
            '" Другое\\n\\nВыберите группу:"',
            '" Другое\\nВыберите группу:"',
            "ui/misc",
            1,
        ),
    ]

    for old, new, label, expected in replacements:
        ui = replace_exact(ui, old, new, label, expected)

    return {card_path: card, ui_path: ui}


def backup_path(path: Path) -> Path:
    return path.with_name(path.name + BACKUP_SUFFIX)


def check(root: Path) -> None:
    changes = build_changes(root)
    print("UI-018 v4: проверка пройдена.")
    for path in changes:
        print(f"  готов: {path.relative_to(root)}")


def apply(root: Path) -> None:
    changes = build_changes(root)

    for path in changes:
        backup = backup_path(path)
        if backup.exists():
            raise FileExistsError(
                f"Уже существует резервная копия: {backup}. "
                "Сначала выполните --revert."
            )

    for path, new_text in changes.items():
        shutil.copy2(path, backup_path(path))
        path.write_text(new_text, encoding="utf-8", newline="")
        print(f"изменён: {path.relative_to(root)}")

    print("UI-018 v4 применён.")
    print("Проверьте: git diff --check")
    print(
        "Затем: git diff -- "
        "OSBB/tools/cashier_v2_telegram/cashier_card.py "
        "OSBB/tools/cashier_v2_telegram/cashier_v2_ui.py"
    )


def revert(root: Path) -> None:
    restored = 0
    for rel in (REL_CARD, REL_UI):
        path = root / rel
        backup = backup_path(path)
        if backup.exists():
            shutil.copy2(backup, path)
            backup.unlink()
            restored += 1
            print(f"восстановлен: {path.relative_to(root)}")
    if restored == 0:
        raise FileNotFoundError("Резервные копии UI-018 v4 не найдены.")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--revert", action="store_true")
    args = parser.parse_args()

    try:
        root = find_root(Path.cwd())
        if args.revert:
            revert(root)
        elif args.check:
            check(root)
        else:
            apply(root)
        return 0
    except Exception as exc:
        print(f"UI-018 v4 ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
