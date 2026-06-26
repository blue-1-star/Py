"""
Подключает многоязычный клиентский кабинет и заявки на пульты к текущему parking_bot.py.

Изменения:
1) импорт handlers.client_portal;
2) show_client_menu() использует меню текущего языка;
3) после выбора языка клиент обязан пользоваться кнопками выбранного языка;
4) client portal вызывается до старого RU-only клиентского раздела;
5) в admin-режиме обрабатывается «🔑 Заявки на пульты».

Старый parking_bot.py не заменяется целиком. Перед применением создаётся backup.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import shutil


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"
PORTAL_FILE = ROOT / "Bots" / "handlers" / "client_portal.py"

IMPORT_BLOCK = (
    "from handlers.client_portal import (\n"
    "    handle_client_portal_text,\n"
    "    client_menu_keyboard,\n"
    "    client_welcome_text,\n"
    ")\n"
)

CLIENT_MENU_FUNCTION = """async def show_client_menu(update: Update, lang: str):
    await update.message.reply_text(
        client_welcome_text(lang),
        reply_markup=kb(client_menu_keyboard(lang)),
    )
"""

LANGUAGE_GATE = """    # =========================
    # Строгий выбор языка для клиентского кабинета
    # =========================
    # После перезапуска язык выбирается заново: это намеренно.
    # До выбора языка не допускаем переход в русское меню «по умолчанию».
    if user_id not in user_languages:
        await update.message.reply_text(
            TEXTS["ru"]["choose_language"],
            reply_markup=kb(LANG_MENU),
        )
        return

"""

PORTAL_ROUTER = """    # =========================
    # Клиентский кабинет / заявки на пульты
    # =========================
    # В client-режиме блокирует старую RU-only обработку кнопок:
    # на каждом уровне принимаются только кнопки выбранного языка.
    # В admin-режиме обрабатывает только «Заявки на пульты».
    if await handle_client_portal_text(
        update,
        user_states,
        user_id,
        text,
        lang=lang,
        user_mode=user_modes.get(user_id),
        is_admin=is_admin_user(user_id),
    ):
        return

"""


def backup_name(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return path.with_name(f"{path.stem}_before_client_portal_{stamp}{path.suffix}")


def patch_import(source: str) -> tuple[str, bool]:
    if "from handlers.client_portal import" in source:
        return source, False

    marker = "from handlers.audit_viewer import handle_audit_viewer_text\n"
    if marker in source:
        return source.replace(marker, marker + IMPORT_BLOCK, 1), True

    lines = source.splitlines(keepends=True)
    handler_lines = [
        idx for idx, line in enumerate(lines)
        if line.startswith("from handlers.")
    ]
    if not handler_lines:
        raise RuntimeError("Не найдено место для import handlers.client_portal.")
    lines.insert(handler_lines[-1] + 1, IMPORT_BLOCK)
    return "".join(lines), True


def patch_show_client_menu(source: str) -> tuple[str, bool]:
    start = source.find("async def show_client_menu(update: Update, lang: str):")
    if start < 0:
        raise RuntimeError("Не найдена функция show_client_menu.")

    end = source.find("\n\nasync def show_admin_menu", start)
    if end < 0:
        raise RuntimeError("Не найден конец функции show_client_menu.")

    old = source[start:end]
    if "client_menu_keyboard(lang)" in old:
        return source, False

    return source[:start] + CLIENT_MENU_FUNCTION.rstrip() + source[end:], True


def patch_language_gate(source: str) -> tuple[str, bool]:
    if "Строгий выбор языка для клиентского кабинета" in source:
        return source, False

    marker = "    t = TEXTS[lang]\n"
    if marker not in source:
        raise RuntimeError("Не найдено место для строгой проверки языка.")

    return source.replace(marker, LANGUAGE_GATE + marker, 1), True


def patch_portal_router(source: str) -> tuple[str, bool]:
    if "handle_client_portal_text(" in source:
        return source, False

    marker = (
        "    # =========================\n"
        "    # Навигация\n"
        "    # =========================\n"
    )
    if marker not in source:
        raise RuntimeError("Не найдено место для подключения client portal.")

    return source.replace(marker, PORTAL_ROUTER + marker, 1), True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("PATCH PARKING BOT: STRICT CLIENT PORTAL + REMOTE REQUESTS")
    print("=" * 100)
    print("Bot:", BOT_FILE)
    print("Portal:", PORTAL_FILE)
    print("Apply:", args.apply)

    if not BOT_FILE.exists():
        raise SystemExit(f"Не найден parking_bot.py: {BOT_FILE}")
    if not PORTAL_FILE.exists():
        raise SystemExit(
            "Не найден Bots/handlers/client_portal.py. "
            "Сначала скопируйте новый handler."
        )

    original = BOT_FILE.read_text(encoding="utf-8")
    patched = original

    patched, import_added = patch_import(patched)
    patched, client_menu_changed = patch_show_client_menu(patched)
    patched, language_gate_added = patch_language_gate(patched)
    patched, router_added = patch_portal_router(patched)

    try:
        compile(patched, str(BOT_FILE), "exec")
    except SyntaxError as exc:
        raise SystemExit(
            f"После patcher код не компилируется: {exc}\n"
            "Исходный parking_bot.py не изменён."
        )

    print("Import added:", import_added)
    print("Client menu localized:", client_menu_changed)
    print("Language gate added:", language_gate_added)
    print("Portal router added:", router_added)
    print("Changes needed:", patched != original)

    if not args.apply:
        print()
        print("DRY RUN COMPLETED - NO CHANGES SAVED")
        return

    if patched == original:
        print()
        print("ALREADY PATCHED - NO FILE CHANGE")
        return

    backup = backup_name(BOT_FILE)
    shutil.copy2(BOT_FILE, backup)
    BOT_FILE.write_text(patched, encoding="utf-8")

    print("Backup:", backup)
    print("APPLIED")


if __name__ == "__main__":
    main()
