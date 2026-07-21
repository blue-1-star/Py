"""
Упрощение приёма наличных в кабинете охранника O.

Новое поведение:
- после суммы сразу показывается предпросмотр;
- стандартная запись создаётся автоматически:
  «Принято наличными на посту O.»;
- охраннику не нужно вручную писать «передано лично за июль»;
- поле «📝 Примечание» остаётся только для исключений;
- в поле примечания символ . или - возвращает стандартную запись.

Скрипт меняет только Bots\handlers\guard_workspace.py при --apply.
Базу данных и parking_bot.py не меняет.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "Bots" / "handlers" / "guard_workspace.py"

NEW_PREVIEW = """async def _show_manual_cash_preview(update: Update, state: dict) -> None:
    state["mode"] = "manual_cash_review"
    unit = state["unit"]
    service = state["service"]
    note = text(state.get("note"))
    note_display = note or "Стандартная запись: принято наличными на посту O."
    await update.message.reply_text(
        "\\n".join([
            "💵 Предпросмотр приёма наличных",
            "",
            f"Касса: O — охрана",
            f"Квартира: {unit.get('apartment_number')}",
            f"Период: {state.get('period_code') or 'не указан'}",
            f"Услуга: {service_label(service)}",
            f"Сумма: {money(state['amount'])} грн.",
            f"Примечание: {note_display}",
            "",
            "Оплата будет создана как неразнесённая.",
            "Охранник не может самостоятельно менять начисления или распределять платёж.",
        ]),
        reply_markup=kb([
            ["✅ Принять наличные в O"],
            ["✏️ Сумма", "📝 Примечание"],
            ["❌ Отменить", HOME],
        ]),
    )
"""

NEW_CASH_FLOW = """    if mode == "manual_cash_amount":
        try:
            state["amount"] = parse_amount(message_text)
        except Exception as exc:
            await update.message.reply_text(f"Ошибка: {exc}")
            return True

        # Обычная операция уже документирована структурированными полями:
        # касса, квартира, период, услуга, сумма, время и охранник.
        # Свободный текст нужен только для исключений.
        state.setdefault("note", "")
        await _show_manual_cash_preview(update, state)
        return True

    if mode == "manual_cash_note":
        # Точка или дефис: оставить системную стандартную отметку.
        state["note"] = "" if message_text in {".", "-"} else message_text
        await _show_manual_cash_preview(update, state)
        return True

"""

NEW_REVIEW_NOTE = """        if message_text in {"📝 Примечание", "📝 Основание"}:
            state["mode"] = "manual_cash_note"
            await update.message.reply_text(
                "Введите короткое примечание только для исключения.\\n"
                "Отправьте . или - — система оставит стандартную запись.",
                reply_markup=kb([["."], [BACK, HOME]]),
            )
            return True

"""


def replace_between(source: str, start: str, end: str, replacement: str) -> str:
    left = source.find(start)
    if left < 0:
        raise RuntimeError(f"Не найден блок начала: {start}")
    right = source.find(end, left)
    if right < 0:
        raise RuntimeError(f"Не найден блок конца: {end}")
    return source[:left] + replacement + source[right:]


def patch(source: str) -> str:
    source = replace_between(
        source,
        "async def _show_manual_cash_preview(",
        "async def _save_manual_cash(",
        NEW_PREVIEW + "\n\n",
    )

    save_start = source.find(
        "    note = text(state.get(\"note\"))",
        source.find("async def _save_manual_cash("),
    )
    save_end = source.find("    conn = get_conn()", save_start)
    if save_start < 0 or save_end < 0:
        raise RuntimeError("Не найдено старое обязательное поле основания.")

    source = (
        source[:save_start]
        + '    note = text(state.get("note")) or "Принято наличными на посту O."\n\n'
        + source[save_end:]
    )

    source = replace_between(
        source,
        '    if mode == "manual_cash_amount":',
        '    if mode == "manual_cash_review":',
        NEW_CASH_FLOW,
    )

    review_start = source.find('    if mode == "manual_cash_review":')
    note_start = source.find('        if message_text == "📝 Основание":', review_start)
    note_end = source.find('        if message_text == "❌ Отменить":', note_start)
    if note_start < 0 or note_end < 0:
        raise RuntimeError("Не найдена ветка редактирования основания.")
    source = source[:note_start] + NEW_REVIEW_NOTE + source[note_end:]

    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("GUARD WORKSPACE: DEFAULT CASH NOTE")
    print("=" * 100)
    print("Target:", TARGET)
    print("Apply:", args.apply)

    if not TARGET.exists():
        print("Не найден:", TARGET)
        return 1

    original = TARGET.read_text(encoding="utf-8")
    try:
        updated = patch(original)
        compile(updated, str(TARGET), "exec")
        print("Patch: OK (compiled in memory)")
    except Exception as exc:
        print("Patch: FAILED")
        print(exc)
        return 1

    if not args.apply:
        print("DRY RUN COMPLETED - NO FILES AND NO DATABASES WERE CHANGED")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = TARGET.with_name(
        f"{TARGET.stem}_before_default_cash_note_{stamp}{TARGET.suffix}"
    )
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding="utf-8")
    print("APPLIED")
    print("Backup:", backup)
    print("Updated:", TARGET)
    print("No database or parking_bot.py was modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
