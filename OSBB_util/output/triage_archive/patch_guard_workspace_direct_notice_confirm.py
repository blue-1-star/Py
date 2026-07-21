"""
Упрощение подтверждения уведомления жителя в кабинете охранника O.

Новое поведение:
- охранник нажимает «✅ Деньги приняты в O»;
- уведомление подтверждается сразу;
- не нужно искать «-» и писать текстовую отметку;
- структурированные поля уже фиксируют квартиру, сумму, период, услугу,
  кассу O, время и Telegram ID охранника.

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

OLD_NOTICE_CARD_BRANCH = """    if mode == "notice_card":
        if message_text == "✅ Деньги приняты в O":
            state["mode"] = "notice_note"
            await update.message.reply_text(
                "Введите короткую отметку охранника или «-».",
                reply_markup=kb([["⬅️ К поступлениям"], [HOME]]),
            )
            return True
        if message_text == "⬅️ К поступлениям":
            await _show_cash_notices(update, state, user_id)
            return True
        await update.message.reply_text("Выберите действие кнопкой.")
        return True

    if mode == "notice_note":
        await _confirm_notice(update, state, user_id, message_text)
        return True
"""

NEW_NOTICE_CARD_BRANCH = """    if mode == "notice_card":
        if message_text == "✅ Деньги приняты в O":
            # Для обычной операции отдельный текст не нужен:
            # факт подтверждения, охранник, касса, сумма и время записываются
            # системой. Исключения будут оформляться отдельным действием.
            await _confirm_notice(update, state, user_id, "")
            return True
        if message_text == "⬅️ К поступлениям":
            await _show_cash_notices(update, state, user_id)
            return True
        await update.message.reply_text("Выберите действие кнопкой.")
        return True

    # Совместимость с незавершённым старым диалогом:
    # если бот был перезапущен именно на старом шаге note, «.» или «-»
    # завершит его без свободного текста.
    if mode == "notice_note":
        await _confirm_notice(
            update,
            state,
            user_id,
            "" if message_text in {".", "-"} else message_text,
        )
        return True
"""


def patch(source: str) -> str:
    if OLD_NOTICE_CARD_BRANCH not in source:
        raise RuntimeError(
            "Не найдена ожидаемая ветка подтверждения уведомления. "
            "Исходный файл не менялся."
        )
    updated = source.replace(
        OLD_NOTICE_CARD_BRANCH,
        NEW_NOTICE_CARD_BRANCH,
        1,
    )
    if "Введите короткую отметку охранника или «-»." in updated:
        raise RuntimeError(
            "Старая обязательная отметка осталась в исходнике. "
            "Исходный файл не менялся."
        )
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("GUARD WORKSPACE: DIRECT NOTICE CONFIRM")
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
        f"{TARGET.stem}_before_direct_notice_confirm_{stamp}{TARGET.suffix}"
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
