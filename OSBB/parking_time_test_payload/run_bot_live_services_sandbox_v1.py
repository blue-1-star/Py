# -*- coding: utf-8 -*-
"""
Launch the real service-order test workflow in the dedicated live-services
sandbox database.

This revision is reinstalled after the two-barrier phone-access V2 source layer
to guarantee that cashier v2 is dispatched before the broad client-portal fallback.

This runner:
- uses only the known live-services sandbox database;
- switches the bot to cashier v2 in memory;
- connects service_orders_workspace to parking_bot in memory;
- uses the simplified paid-preorder workspace installed in Bots/handlers;
- prepares sandbox-only service permissions for test operators;
- never changes Bots\\parking_bot.py or config.py.

It is intentionally separate from the old Guard Sandbox runner.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import os
import shutil
import sqlite3
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"
BACKUP_DIR = SANDBOX_DIR / "backups"

LIVE_SERVICES_DB = (
    SANDBOX_DIR / "osbb_test_live_services_2026-06-26_20-13-26.db"
)

BOT_FILE = BOTS_DIR / "parking_bot.py"
WORKSPACE_FILE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
V2_SWITCHER = ROOT / "switch_parking_bot_to_cashier_v2.py"
SERVICE_PATCHER = ROOT / "patch_parking_bot_service_orders_v1.py"
PROFILE_CORE_FILE = ROOT / "profile_verification_core.py"
PROFILE_WORKSPACE_FILE = BOTS_DIR / "handlers" / "profile_verification_workspace.py"
PROFILE_TEST_CORE_FILE = ROOT / "profile_parking_time_test_core.py"
PROFILE_TEST_WORKSPACE_FILE = (
    BOTS_DIR / "handlers" / "profile_parking_time_test_workspace.py"
)

# 210312208 accepted the resident remote in SO-20260626-000001.
# Configured admins are added automatically as well.
KNOWN_TEST_OPERATOR_IDS = {210312208}
SANDBOX_SERVICE_ROLE = "SERVICE_OPERATOR_SANDBOX"


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось загрузить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def clone_paths(original: Any, sandbox_db: Path) -> Any:
    try:
        cloned = copy.copy(original)
        if cloned is original:
            raise RuntimeError
    except Exception:
        values = {
            name: getattr(original, name)
            for name in dir(original)
            if not name.startswith("_") and not callable(getattr(original, name))
        }
        cloned = SimpleNamespace(**values)

    setattr(cloned, "OSBB_TEST_DB_FILE", sandbox_db)
    return cloned


def configure_sandbox(sandbox_db: Path) -> None:
    for folder in (ROOT, BOTS_DIR, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config

    original_test = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
    original_prod = Path(config.paths.OSBB_DB_FILE).resolve()
    if sandbox_db.resolve() in {original_test, original_prod}:
        raise RuntimeError(
            "Отказ: этот launcher разрешает только отдельную sandbox-БД, "
            "не основную базу и не штатную test-БД."
        )

    config.paths = clone_paths(config.paths, sandbox_db)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox_db)
    os.environ["OSBB_SANDBOX_MODE"] = "1"
    os.environ["OSBB_LIVE_SERVICES_SANDBOX"] = "1"

    if str(config.paths.SECRETS_DIR) not in sys.path:
        sys.path.insert(0, str(config.paths.SECRETS_DIR))


def tables(conn: sqlite3.Connection) -> set[str]:
    return {
        str(row[0])
        for row in conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
    }


def columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    safe_name = str(table_name).replace('"', '""')
    return {
        str(row[1])
        for row in conn.execute(f'PRAGMA table_info("{safe_name}")').fetchall()
    }


def create_backup(db_path: Path, reason: str) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = BACKUP_DIR / f"{db_path.stem}_before_{reason}_{stamp}{db_path.suffix}"
    shutil.copy2(db_path, backup)
    return backup


def configured_operator_ids() -> list[int]:
    user_ids = set(KNOWN_TEST_OPERATOR_IDS)
    try:
        from telegram_osbb import ADMIN_IDS, SUPER_ADMIN_IDS

        for raw_id in tuple(ADMIN_IDS) + tuple(SUPER_ADMIN_IDS):
            try:
                user_ids.add(int(raw_id))
            except (TypeError, ValueError):
                pass
    except Exception as exc:
        print(f"WARNING: unable to read configured admin IDs: {exc}")

    return sorted(user_ids)


def ensure_sandbox_service_access(db_path: Path) -> tuple[list[int], list[str], Path | None]:
    """
    Give configured test operators only the sandbox permissions required by the
    simplified paid-preorder workflow.

    No resident order, payment, interest, supplier batch or remote record is
    changed here. The sole possible database changes are role/permission rows.
    """
    conn = sqlite3.connect(db_path)
    try:
        present = tables(conn)
        required = {"access_user_roles", "access_role_permissions"}
        missing = sorted(required - present)
        if missing:
            return [], [
                "permissions not seeded: missing tables " + ", ".join(missing)
            ], None

        user_role_columns = columns(conn, "access_user_roles")
        permission_columns = columns(conn, "access_role_permissions")
        expected_user_columns = {
            "telegram_user_id", "role_code", "scope_type", "scope_value",
            "is_active",
        }
        expected_permission_columns = {
            "role_code", "resource", "action", "scope_type", "scope_value",
            "effect", "is_active",
        }
        if not expected_user_columns.issubset(user_role_columns):
            return [], [
                "permissions not seeded: access_user_roles schema is incompatible"
            ], None
        if not expected_permission_columns.issubset(permission_columns):
            return [], [
                "permissions not seeded: access_role_permissions schema is incompatible"
            ], None

        requested_users = configured_operator_ids()

        # The operator UI checks these rights by SERVICE_CATEGORY.
        category_permissions: list[tuple[str, str, str]] = [
            ("service_orders", "VIEW", "REMOTE"),
            ("service_orders", "CREATE", "REMOTE"),
            ("service_orders", "UPDATE", "REMOTE"),
            ("service_orders", "CONFIRM", "REMOTE"),
            ("service_order_steps", "VIEW", "REMOTE"),
            ("service_order_steps", "CREATE", "REMOTE"),
            ("service_order_steps", "CONFIRM", "REMOTE"),
            ("service_order_payment_links", "VIEW", "REMOTE"),
            ("service_order_payment_links", "CREATE", "REMOTE"),
            ("service_orders", "VIEW", "ACCESS"),
            ("service_orders", "CREATE", "ACCESS"),
            ("service_orders", "UPDATE", "ACCESS"),
            ("service_orders", "CONFIRM", "ACCESS"),
            ("service_order_steps", "VIEW", "ACCESS"),
            ("service_order_steps", "CREATE", "ACCESS"),
            ("service_order_steps", "CONFIRM", "ACCESS"),
            ("service_order_payment_links", "VIEW", "ACCESS"),
            ("service_order_payment_links", "CREATE", "ACCESS"),
            ("service_access_credentials", "VIEW", "ACCESS"),
            ("service_access_credentials", "CREATE", "ACCESS"),
            ("service_access_credentials", "ACTIVATE", "ACCESS"),
        ]

        # Physical remote movements are controlled by guard post O, not by
        # service category. They cover receipt, return, and post-delivery issue.
        post_permissions: list[tuple[str, str, str, str]] = [
            ("remote_assets", "VIEW", "POST", "O"),
            ("remote_assets", "CREATE", "POST", "O"),
            ("remote_assets", "UPDATE", "POST", "O"),
            ("remote_assets", "MOVE", "POST", "O"),
            ("remote_asset_movements", "VIEW", "POST", "O"),
            ("remote_asset_movements", "CREATE", "POST", "O"),
        ]

        changes: list[str] = []
        needs_change = False

        for user_id in requested_users:
            exists = conn.execute(
                """
                SELECT 1
                FROM access_user_roles
                WHERE telegram_user_id = ?
                  AND role_code = ?
                  AND scope_type = 'ALL'
                  AND scope_value = '*'
                  AND COALESCE(is_active, 1) = 1
                LIMIT 1
                """,
                (str(user_id), SANDBOX_SERVICE_ROLE),
            ).fetchone()
            if not exists:
                needs_change = True

        def has_permission_row(
            resource: str,
            action: str,
            scope_type: str,
            scope_value: str,
        ) -> bool:
            return conn.execute(
                """
                SELECT 1
                FROM access_role_permissions
                WHERE role_code = ?
                  AND resource = ?
                  AND action = ?
                  AND scope_type = ?
                  AND scope_value = ?
                  AND effect = 'ALLOW'
                  AND COALESCE(is_active, 1) = 1
                LIMIT 1
                """,
                (
                    SANDBOX_SERVICE_ROLE,
                    resource,
                    action,
                    scope_type,
                    scope_value,
                ),
            ).fetchone() is not None

        for resource, action, category in category_permissions:
            if not has_permission_row(
                resource, action, "SERVICE_CATEGORY", category
            ):
                needs_change = True

        for resource, action, scope_type, scope_value in post_permissions:
            if not has_permission_row(
                resource, action, scope_type, scope_value
            ):
                needs_change = True

        backup: Path | None = None
        if needs_change:
            backup = create_backup(db_path, "simplified_service_permissions")

            for user_id in requested_users:
                exists = conn.execute(
                    """
                    SELECT 1
                    FROM access_user_roles
                    WHERE telegram_user_id = ?
                      AND role_code = ?
                      AND scope_type = 'ALL'
                      AND scope_value = '*'
                      AND COALESCE(is_active, 1) = 1
                    LIMIT 1
                    """,
                    (str(user_id), SANDBOX_SERVICE_ROLE),
                ).fetchone()
                if not exists:
                    conn.execute(
                        """
                        INSERT INTO access_user_roles
                            (telegram_user_id, role_code, scope_type, scope_value,
                             is_active, note, created_at, updated_at)
                        VALUES (?, ?, 'ALL', '*', 1, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """,
                        (
                            str(user_id),
                            SANDBOX_SERVICE_ROLE,
                            "Sandbox role for simplified service-workflow testing.",
                        ),
                    )
                    changes.append(f"role assigned to Telegram ID {user_id}")

            permission_specs = [
                (
                    resource,
                    action,
                    "SERVICE_CATEGORY",
                    category,
                )
                for resource, action, category in category_permissions
            ] + post_permissions

            for resource, action, scope_type, scope_value in permission_specs:
                if has_permission_row(resource, action, scope_type, scope_value):
                    continue
                conn.execute(
                    """
                    INSERT INTO access_role_permissions
                        (role_code, resource, action, scope_type, scope_value,
                         effect, is_active, note, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, 'ALLOW', 1, ?,
                            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """,
                    (
                        SANDBOX_SERVICE_ROLE,
                        resource,
                        action,
                        scope_type,
                        scope_value,
                        "Sandbox-only simplified-service workflow permission.",
                    ),
                )
                changes.append(
                    f"permission {resource}/{action}/{scope_type}:{scope_value}"
                )

            conn.commit()

        return requested_users, changes, backup
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def assert_workspace_is_compatible() -> None:
    """
    Verify the current simplified paid-preorder workspace.

    The old launcher looked for retired manual payment-link markers. The new
    workflow deliberately promotes a paid interest after cashier confirmation,
    so it must be checked by its new supplier/preorder capabilities instead.
    """
    if not WORKSPACE_FILE.is_file():
        raise FileNotFoundError(f"Не найден модуль услуг: {WORKSPACE_FILE}")

    source = WORKSPACE_FILE.read_text(encoding="utf-8")
    required = (
        "from service_preorders_core import (",
        "def _ensure_and_reconcile() -> None:",
        "reconcile_paid_service_interests(conn=conn)",
        "NEW_REMOTE_PROFILE",
        "create_supplier_batch(",
        "receive_supplier_batch(",
        "issue_new_remotes_from_batch(",
    )
    missing = [marker for marker in required if marker not in source]
    if missing:
        raise RuntimeError(
            "В service_orders_workspace.py не установлена готовая версия "
            "оплаченных предзаказов. Не хватает: " + ", ".join(missing)
        )
    compile(source, str(WORKSPACE_FILE), "exec")

def purge_project_modules() -> None:
    exact_names = {
        "cashier_v2_core",
        "access_control",
        "audit_logger",
        "db_access",
        "Bots.db_access",
        "service_orders_core",
        "service_preorders_core",
        "handlers.client_portal",
        "handlers.client_portal_v2",
        "handlers.cashier_operator",
        "handlers.cashier_operator_v2",
        "handlers.service_orders_workspace",
        "handlers.profile_verification_workspace",
        "profile_verification_core",
        "handlers.profile_parking_time_test_workspace",
        "profile_parking_time_test_core",
        "handlers.guard_workspace",
    }
    for name in list(sys.modules):
        if name in exact_names:
            sys.modules.pop(name, None)




def integrate_profile_verification(source: str) -> tuple[str, list[str]]:
    """Patch profile verification into the bot source in memory only."""
    changes: list[str] = []

    import_anchor = "from handlers.cashier_operator_v2 import handle_cashier_operator_v2_text"
    profile_import = (
        "from handlers.profile_verification_workspace import (\n"
        "    handle_profile_verification_text,\n"
        "    maybe_show_profile_welcome,\n"
        "    show_profile_verification,\n"
        ")\n"
    )
    if "from handlers.profile_verification_workspace import (" not in source:
        index = source.find(import_anchor)
        if index < 0:
            raise RuntimeError("Не найден импорт cashier v2 для подключения проверки данных.")
        source = source[:index] + profile_import + source[index:]
        changes.append("profile verification import")

    test_import = (
        "from handlers.profile_parking_time_test_workspace import "
        "handle_profile_parking_time_test_text\n"
    )
    if "from handlers.profile_parking_time_test_workspace import " not in source:
        index = source.find(import_anchor)
        if index < 0:
            raise RuntimeError("Не найден импорт cashier v2 для подключения TEST parking_time.")
        source = source[:index] + test_import + source[index:]
        changes.append("parking_time TEST import")

    menu_anchor = "USERS_MENU = ["
    menu_wrapper = r"""
# Runtime extension: keeps v2 menu and adds data review entries.
_profile_original_client_menu_keyboard = client_menu_keyboard

def client_menu_keyboard(lang: str):
    rows = [list(row) for row in _profile_original_client_menu_keyboard(lang)]
    labels = {
        "ru": "📋 Проверить мои данные",
        "uk": "📋 Перевірити мої дані",
        "en": "📋 Verify my data",
    }
    label = labels.get(lang, labels["ru"])
    if not any(label in row for row in rows):
        admin_index = next(
            (i for i, row in enumerate(rows) if any("Админ" in cell or "Адмін" in cell or "Admin" in cell for cell in row)),
            len(rows),
        )
        rows.insert(admin_index, [label])
    return rows

if not any(
    any("Проверка данных" in cell or "Перевірка даних" in cell for cell in row)
    for row in ADMIN_MENU
):
    ADMIN_MENU.insert(5, ["📋 Проверка данных жителей"])

if not any(
    any("TEST parking_time" in cell or "Тест parking_time" in cell for cell in row)
    for row in ADMIN_MENU
):
    ADMIN_MENU.insert(6, ["🧪 Тест parking_time"])

"""
    if "_profile_original_client_menu_keyboard = client_menu_keyboard" not in source:
        index = source.find(menu_anchor)
        if index < 0:
            raise RuntimeError("Не найдено место для расширения меню проверки данных.")
        source = source[:index] + menu_wrapper + source[index:]
        changes.append("profile buttons in client/admin menus")

    old_show = """async def show_client_menu(update: Update, lang: str):
    await update.message.reply_text(
        client_welcome_text(lang),
        reply_markup=kb(client_menu_keyboard(lang)),
    )
"""
    new_show = """async def show_client_menu(update: Update, lang: str):
    await update.message.reply_text(
        client_welcome_text(lang),
        reply_markup=kb(client_menu_keyboard(lang)),
    )
    await maybe_show_profile_welcome(
        update,
        user_states,
        update.effective_user.id,
        lang=lang,
    )
"""
    if old_show in source:
        source = source.replace(old_show, new_show, 1)
        changes.append("one-time profile welcome")
    elif "await maybe_show_profile_welcome(" not in source:
        raise RuntimeError("Не найден show_client_menu для приветствия проверки данных.")

    direct_router_anchor = (
        "    # =========================\n"
        "    # Реестр помещений\n"
    )
    test_router = r"""    # =========================
    # Ізольований TEST parking_time
    # =========================
    # Admin-only. This handler writes only to dedicated TEST tables and never
    # opens the target apartment as a resident.
    if await handle_profile_parking_time_test_text(
        update,
        user_states,
        user_id,
        text,
        lang=lang,
        is_admin=is_admin_user(user_id),
    ):
        return

"""
    if "# Ізольований TEST parking_time" not in source:
        index = source.find(direct_router_anchor)
        if index < 0:
            raise RuntimeError("Не найден ранний раздел для TEST parking_time.")
        source = source[:index] + test_router + source[index:]
        changes.append("parking_time TEST route before legacy states")

    direct_router = r"""    # =========================
    # Прямая кнопка перевірки даних
    # =========================
    # This runs before legacy state routers. A resident may always open the
    # verification card even if a former service/cashier state was left open.
    if text in {
        "📋 Проверить мои данные",
        "📋 Перевірити мої дані",
        "📋 Verify my data",
    }:
        await show_profile_verification(
            update,
            user_states,
            user_id,
            lang=lang,
        )
        return

"""
    if "# Прямая кнопка перевірки даних" not in source:
        index = source.find(direct_router_anchor)
        if index < 0:
            raise RuntimeError(
                "Не найден ранний раздел для прямой кнопки проверки данных."
            )
        source = source[:index] + direct_router + source[index:]
        changes.append("direct profile button before legacy states")

    client_header = (
        "    # =========================\n"
        "    # Клиентский кабинет / заявки на пульты\n"
    )
    profile_section = r"""    # =========================
    # Перевірка даних мешканця
    # =========================
    # Handles states inside the profile card after its direct button was
    # intercepted above. It never compares a private barrier-access phone
    # with resident contact numbers.
    if await handle_profile_verification_text(
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
    if "await handle_profile_verification_text(" not in source:
        index = source.find(client_header)
        if index < 0:
            raise RuntimeError("Не найден клиентский раздел для маршрута проверки данных.")
        source = source[:index] + profile_section + source[index:]
        changes.append("profile route before client portal")

    compile(source, str(BOT_FILE), "exec")
    return source, changes

def ensure_cashier_route_precedes_client_portal(source: str) -> tuple[str, bool]:
    """
    The client portal has a broad fallback for menu text. Therefore the cash
    handler must run first; otherwise a press on '💰 Касса' is acknowledged by
    the portal instead of opening cashier v2.

    This changes only the in-memory source executed by the live-services
    sandbox launcher. Bots/parking_bot.py is not written to disk.
    """
    client_header = (
        "    # =========================\n"
        "    # Клиентский кабинет / заявки на пульты\n"
    )
    cashier_header = (
        "    # =========================\n"
        "    # Операторский кассовый редактор\n"
    )
    navigation_header = (
        "    # =========================\n"
        "    # Навигация\n"
    )

    client_start = source.find(client_header)
    cashier_start = source.find(cashier_header)
    if min(client_start, cashier_start) < 0:
        raise RuntimeError(
            "Не найдены ожидаемые разделы client portal / cashier в parking_bot.py."
        )

    # The desired order is already present.
    if cashier_start < client_start:
        return source, False

    navigation_start = source.find(navigation_header, cashier_start + 1)
    if navigation_start < 0:
        raise RuntimeError(
            "Не найден следующий раздел навигации в parking_bot.py."
        )

    client_section = source[client_start:cashier_start]
    cashier_section = source[cashier_start:navigation_start]

    required = (
        "await handle_client_portal_text(",
        "await handle_cashier_operator_v2_text(",
    )
    missing = [
        marker
        for marker in required
        if marker not in client_section + cashier_section
    ]
    if missing:
        raise RuntimeError(
            "В parking_bot.py не найдены обработчики для перестановки: "
            + ", ".join(missing)
        )

    return (
        source[:client_start]
        + cashier_section.rstrip()
        + "\n\n"
        + client_section.rstrip()
        + "\n\n"
        + source[navigation_start:],
        True,
    )

def patch_bot_source() -> tuple[str, list[str]]:
    if not BOT_FILE.is_file():
        raise FileNotFoundError(f"Не найден parking_bot.py: {BOT_FILE}")
    if not V2_SWITCHER.is_file():
        raise FileNotFoundError(f"Не найден v2 switcher: {V2_SWITCHER}")
    if not SERVICE_PATCHER.is_file():
        raise FileNotFoundError(f"Не найден service patcher: {SERVICE_PATCHER}")
    if not PROFILE_CORE_FILE.is_file():
        raise FileNotFoundError(f"Не найдено ядро проверки данных: {PROFILE_CORE_FILE}")
    if not PROFILE_WORKSPACE_FILE.is_file():
        raise FileNotFoundError(f"Не найден интерфейс проверки данных: {PROFILE_WORKSPACE_FILE}")
    if not PROFILE_TEST_CORE_FILE.is_file():
        raise FileNotFoundError(f"Не найдено TEST-ядро parking_time: {PROFILE_TEST_CORE_FILE}")
    if not PROFILE_TEST_WORKSPACE_FILE.is_file():
        raise FileNotFoundError(
            f"Не найден TEST-интерфейс parking_time: {PROFILE_TEST_WORKSPACE_FILE}"
        )

    source = BOT_FILE.read_text(encoding="utf-8")
    v2 = load_module(V2_SWITCHER, "_live_services_v2_switcher")
    service = load_module(SERVICE_PATCHER, "_live_services_router_patcher")

    source, v2_changes = v2.patch(source)
    source, service_changes = service.patch(source)
    source, profile_changes = integrate_profile_verification(source)
    source, cashier_first = ensure_cashier_route_precedes_client_portal(source)
    compile(source, str(BOT_FILE), "exec")

    return source, [
        "cashier v2: " + ("; ".join(v2_changes) if v2_changes else "already active"),
        "service orders: " + (
            "; ".join(service_changes) if service_changes else "already integrated"
        ),
        "profile verification: " + (
            "; ".join(profile_changes) if profile_changes else "already integrated"
        ),
        (
            "cashier route: placed before client portal"
            if cashier_first
            else "cashier route: already before client portal"
        ),
    ]


def live_service_preflight(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        present = tables(conn)
        required = {
            "payments",
            "service_orders",
            "service_order_steps",
            "service_order_payment_links",
            "remote_order_details",
            "remote_assets",
            "service_order_interests",
            "remote_supplier_batches",
            "remote_supplier_batch_links",
            "remote_order_issued_assets",
            "resident_profile_verifications",
            "resident_profile_change_requests",
            "profile_parking_time_test_sessions",
            "profile_parking_time_test_events",
        }
        missing = sorted(required - present)
        if missing:
            raise RuntimeError(
                "Это не live-services sandbox. Нет таблиц: " + ", ".join(missing)
            )

        payment_columns = columns(conn, "payments")
        print("Preflight:")
        print(
            "  payments.source_ref:",
            "present" if "source_ref" in payment_columns
            else "not present (compatible mode will be used)",
        )
        print(
            "  payments.apartment_id:",
            "present" if "apartment_id" in payment_columns
            else "not present (apartment_number mode will be used)",
        )

        order = conn.execute(
            """
            SELECT id, order_number, apartment_id, apartment_number,
                   service_item_code, service_name_snapshot,
                   order_status, payment_status, fulfillment_status
            FROM service_orders
            WHERE order_status NOT IN ('COMPLETED', 'CANCELLED')
            ORDER BY id ASC
            LIMIT 1
            """
        ).fetchone()
        if order:
            print(
                "  current open order:",
                f"{order['order_number']} | кв.{order['apartment_number']} | "
                f"{order['service_name_snapshot']} | {order['order_status']}"
            )
            if "apartment_id" in payment_columns:
                payment_where = "apartment_id = ?"
                apartment_value: Any = order["apartment_id"]
            else:
                payment_where = "CAST(apartment_number AS TEXT) = ?"
                apartment_value = str(order["apartment_number"])

            candidates = conn.execute(
                f"""
                SELECT COUNT(*)
                FROM payments
                WHERE {payment_where}
                  AND COALESCE(service_item_code, '') = COALESCE(?, '')
                  AND COALESCE(cashier_entry_status, 'CONFIRMED') = 'CONFIRMED'
                  AND COALESCE(amount, 0) > 0
                """,
                (apartment_value, order["service_item_code"]),
            ).fetchone()[0]
            print("  matching confirmed payments for this order:", int(candidates))
        else:
            print("  current open order: none")
    finally:
        conn.close()


def conflicting_guard_processes() -> list[str]:
    command = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') "
        "-and $_.CommandLine -like '*run_bot_guard_sandbox_v3.py*--run*' } | "
        "ForEach-Object { 'PID=' + $_.ProcessId + ' | ' + $_.CommandLine }"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
    except Exception:
        return []

    return [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]


def run_bot(source: str) -> None:
    os.chdir(BOTS_DIR)
    namespace = {
        "__name__": "__main__",
        "__file__": str(BOT_FILE),
        "__package__": None,
    }
    exec(compile(source, str(BOT_FILE), "exec"), namespace)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument(
        "--no-permission-seed",
        action="store_true",
        help="Do not create sandbox-only service operator permissions.",
    )
    args = parser.parse_args()

    print("=" * 100)
    print("OSBB LIVE SERVICES SANDBOX")
    print("=" * 100)
    print("Database:", LIVE_SERVICES_DB)
    print("Mode:", "RUN TELEGRAM BOT" if args.run else "CHECK ONLY")

    if not LIVE_SERVICES_DB.is_file():
        raise FileNotFoundError(
            "Не найдена live-services sandbox-БД:\n"
            f"  {LIVE_SERVICES_DB}"
        )

    configure_sandbox(LIVE_SERVICES_DB)
    live_service_preflight(LIVE_SERVICES_DB)

    if args.no_permission_seed:
        print("Permission seed: skipped by --no-permission-seed")
    else:
        users, changes, backup = ensure_sandbox_service_access(LIVE_SERVICES_DB)
        print("Sandbox service operator IDs:", ", ".join(map(str, users)) or "(none)")
        if backup:
            print("Sandbox backup before permission seed:", backup)
        print(
            "Permission seed:",
            f"{len(changes)} change(s)" if changes else "already prepared",
        )

    assert_workspace_is_compatible()
    purge_project_modules()
    source, bot_changes = patch_bot_source()

    print("Runtime changes:")
    print("  - service_orders workspace: simplified paid-preorder workflow verified")
    for item in bot_changes:
        print("  -", item)

    if not args.run:
        print()
        print("CHECK PASSED")
        print("No Telegram polling was started.")
        print("Bots\\parking_bot.py and config.py were not changed.")
        return 0

    conflicts = conflicting_guard_processes()
    if conflicts:
        print()
        print("REFUSED: old Guard Sandbox bot process(es) are still polling Telegram:")
        for item in conflicts:
            print("  ", item)
        print("Stop them with Ctrl+C, then run this launcher again.")
        return 2

    print()
    print("Starting live services sandbox bot.")
    print("All order/payment/remote test changes go only to:")
    print(" ", LIVE_SERVICES_DB)
    print("Stop this bot with Ctrl+C.")
    print()
    run_bot(source)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nLive services sandbox bot stopped by Ctrl+C.")
        raise SystemExit(0)
    except Exception:
        print("\nLIVE SERVICES SANDBOX LAUNCH FAILED")
        traceback.print_exc()
        raise SystemExit(1)
