# -*- coding: utf-8 -*-
r'''
Runtime patch for OSBB service orders / remotes / access.

The patch does not change Bots\\parking_bot.py by itself. It adds:
- import of handle_service_orders_text;
- an early service-order route inside message_handler.

It is deliberately independent from the old guard-workspace patch.
'''

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOT_FILE = ROOT / "Bots" / "parking_bot.py"

SERVICE_IMPORT = (
    "from handlers.service_orders_workspace import handle_service_orders_text\n"
)

SERVICE_ROUTE = r'''
    # =========================
    # Пульты, доступ и заявки на услуги
    # =========================
    # Этот маршрут должен быть раньше обычных меню и state-router'ов:
    # service_orders_workspace хранит собственные состояния в user_states.
    if await handle_service_orders_text(
        update,
        user_states,
        user_id,
        text,
        lang=lang,
        user_mode=user_modes.get(user_id),
    ):
        return

'''


def add_import(source: str) -> tuple[str, bool]:
    if "from handlers.service_orders_workspace import handle_service_orders_text" in source:
        return source, False

    anchors = (
        "from handlers.audit_viewer import handle_audit_viewer_text\n",
        "from handlers.unit_registry_editor import handle_unit_registry_editor_text\n",
    )
    for anchor in anchors:
        if anchor in source:
            return source.replace(anchor, anchor + SERVICE_IMPORT, 1), True

    raise RuntimeError(
        "Не найден безопасный якорь импорта для service_orders_workspace."
    )


def add_route(source: str) -> tuple[str, bool]:
    if "await handle_service_orders_text(" in source:
        return source, False

    handler_start = source.find("async def message_handler(")
    if handler_start < 0:
        raise RuntimeError("Не найдена функция message_handler().")

    anchor = "    t = TEXTS[lang]\n"
    position = source.find(anchor, handler_start)
    if position < 0:
        raise RuntimeError(
            "Не найдена строка 't = TEXTS[lang]' внутри message_handler()."
        )

    return (
        source[: position + len(anchor)]
        + SERVICE_ROUTE
        + source[position + len(anchor) :],
        True,
    )


def patch(source: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    source, changed = add_import(source)
    if changed:
        changes.append("service_orders_workspace import")

    source, changed = add_route(source)
    if changed:
        changes.append("service-orders router")

    required = (
        "from handlers.service_orders_workspace import handle_service_orders_text",
        "await handle_service_orders_text(",
        "user_mode=user_modes.get(user_id)",
    )
    missing = [item for item in required if item not in source]
    if missing:
        raise RuntimeError("Патч собран не полностью: " + ", ".join(missing))

    return source, changes
