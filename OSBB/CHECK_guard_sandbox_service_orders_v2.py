# -*- coding: utf-8 -*-
r"""
OSBB — Guard Sandbox / Service Orders diagnostic, version 2.

Place this file directly in:
    G:\Programming\Py\OSBB\

This version does NOT need Start_OSBB_Guard_Sandbox_Bot_v2.bat.
It uses the exact sandbox database selected by that launcher on 27.06.2026.

Read-only:
- does not change any SQLite database;
- does not modify bot source code;
- does not modify config.py;
- creates only a text report in Data\db\logs.
"""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
LOG_DIR = ROOT / "Data" / "db" / "logs"

# Exact sandbox selected by Start_OSBB_Guard_Sandbox_Bot_v2.bat.
SANDBOX_DB = (
    ROOT
    / "Data"
    / "db"
    / "sandbox"
    / "osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db"
)

PARKING_BOT = BOTS_DIR / "parking_bot.py"
WORKSPACE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
V2_SWITCHER = ROOT / "switch_parking_bot_to_cashier_v2.py"
GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"

REPORT: list[str] = []


def say(value: object = "") -> None:
    line = str(value)
    print(line)
    REPORT.append(line)


def separator(char: str = "=") -> None:
    say(char * 100)


def read_source(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1251", "cp866"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Cannot decode file: {path}")


def quote_identifier(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def connect_readonly(db_path: Path) -> sqlite3.Connection:
    uri = "file:" + db_path.resolve().as_posix() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (name,),
    ).fetchone() is not None


def table_columns(conn: sqlite3.Connection, name: str) -> list[str]:
    if not table_exists(conn, name):
        return []
    return [
        str(row["name"])
        for row in conn.execute(f"PRAGMA table_info({quote_identifier(name)})").fetchall()
    ]


def table_count(conn: sqlite3.Connection, name: str) -> int | None:
    if not table_exists(conn, name):
        return None
    return int(
        conn.execute(f"SELECT COUNT(*) FROM {quote_identifier(name)}").fetchone()[0]
    )


def select_rows(
    conn: sqlite3.Connection,
    table: str,
    wanted_columns: Iterable[str],
    *,
    limit: int = 50,
    order_by: Iterable[str] = ("id",),
) -> list[dict[str, Any]]:
    available = table_columns(conn, table)
    if not available:
        return []

    chosen = [column for column in wanted_columns if column in available]
    if not chosen:
        chosen = available[: min(15, len(available))]

    ordering = next((column for column in order_by if column in available), None)
    sql = (
        "SELECT "
        + ", ".join(quote_identifier(column) for column in chosen)
        + f" FROM {quote_identifier(table)}"
    )
    if ordering:
        sql += f" ORDER BY {quote_identifier(ordering)} DESC"
    sql += " LIMIT ?"
    return [
        dict(row)
        for row in conn.execute(sql, (int(limit),)).fetchall()
    ]


def show_rows(title: str, rows: list[dict[str, Any]]) -> None:
    say()
    say(title)
    if not rows:
        say("  (no rows)")
        return
    for row in rows:
        say("  " + " | ".join(f"{key}={value!r}" for key, value in row.items()))


def source_contexts(source: str, marker: str, *, margin: int = 2) -> list[str]:
    lines = source.splitlines()
    blocks: list[str] = []
    for index, row in enumerate(lines):
        if marker.casefold() not in row.casefold():
            continue
        start = max(0, index - margin)
        end = min(len(lines), index + margin + 1)
        blocks.append(
            "\n".join(
                f"{line_number + 1:>5}: {lines[line_number]}"
                for line_number in range(start, end)
            )
        )
    return blocks


def load_module_from_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def inspect_bot_source() -> None:
    separator()
    say("BOT SOURCE / RUNTIME PATCH CHECK")

    for path in (PARKING_BOT, WORKSPACE, V2_SWITCHER, GUARD_PATCHER):
        status = "OK" if path.is_file() else "MISSING"
        say(f"[{status}] {path}")

    if not PARKING_BOT.is_file():
        return

    raw_source = read_source(PARKING_BOT)
    patched_source: str | None = None

    say()
    say(f"Raw parking_bot.py: {len(raw_source.splitlines())} lines")

    if V2_SWITCHER.is_file() and GUARD_PATCHER.is_file():
        try:
            v2 = load_module_from_path(V2_SWITCHER, "_guard_diagnosis_v2_switcher")
            guard = load_module_from_path(GUARD_PATCHER, "_guard_diagnosis_patcher")

            patched_source, v2_changes = v2.patch(raw_source)
            patched_source, guard_changes = guard.patch(patched_source)
            compile(patched_source, str(PARKING_BOT), "exec")

            say("V2 changes: " + ("; ".join(v2_changes) if v2_changes else "(none)"))
            say("Guard changes: " + ("; ".join(guard_changes) if guard_changes else "(none)"))
            say(f"Patched parking_bot.py: {len(patched_source.splitlines())} lines; compile PASS")
        except Exception as exc:  # diagnostics continue with DB inspection
            say(f"PATCH ANALYSIS FAILED: {type(exc).__name__}: {exc}")
            say(traceback.format_exc())

    markers = (
        "service_orders_workspace",
        "handle_service_orders_text",
        "show_service_operator_workspace",
        "🔑 Заявки на пульты",
        "🔑 Оператор услуг",
        "remote_requests",
        "guard_workspace",
    )

    for title, code in (("RAW SOURCE", raw_source), ("PATCHED SOURCE", patched_source)):
        say()
        say(title)
        if code is None:
            say("  (not available)")
            continue
        for marker in markers:
            contexts = source_contexts(code, marker)
            say(f"  {marker!r}: {len(contexts)} occurrence(s)")
            for block in contexts[:3]:
                for text_line in block.splitlines():
                    say("    " + text_line)
                say("    ---")

    if WORKSPACE.is_file():
        workspace_source = read_source(WORKSPACE)
        say()
        say("SERVICE WORKSPACE CHECK")
        say(f"service_orders_workspace.py: {len(workspace_source.splitlines())} lines")
        for marker in (
            "def handle_service_orders_text",
            "🔑 Заявки на пульты",
            "has_service_workspace_access",
            "def _matching_payments",
            "_payments_has_source_ref",
            "p.source_ref",
        ):
            say(f"  {marker!r}: {len(source_contexts(workspace_source, marker))} occurrence(s)")


def inspect_database() -> None:
    separator()
    say("SANDBOX DATABASE CHECK")
    say(f"Sandbox DB: {SANDBOX_DB}")
    say(f"Exists: {SANDBOX_DB.is_file()}")
    if not SANDBOX_DB.is_file():
        return

    conn = connect_readonly(SANDBOX_DB)
    try:
        say("Opened read-only: PASS")

        tables = (
            "payments",
            "service_orders",
            "service_order_steps",
            "service_order_payment_links",
            "remote_order_details",
            "remote_assets",
            "remote_requests",
            "remote_handover_events",
            "staff_principals",
            "access_user_roles",
            "access_user_permissions",
            "access_role_permissions",
            "access_audit_log",
        )

        say()
        say("Relevant tables:")
        for table in tables:
            count = table_count(conn, table)
            if count is None:
                say(f"  [MISSING] {table}")
            else:
                say(f"  [OK] {table}: {count} row(s)")
                say("       columns: " + ", ".join(table_columns(conn, table)))

        if table_exists(conn, "payments"):
            payment_columns = set(table_columns(conn, "payments"))
            say()
            say(
                "payments.source_ref: "
                + ("PRESENT" if "source_ref" in payment_columns else "MISSING")
            )
            show_rows(
                "Latest payments:",
                select_rows(
                    conn,
                    "payments",
                    (
                        "id", "payment_date", "apartment_id", "service_item_code",
                        "amount", "currency", "payment_method", "payment_channel",
                        "cashbox_code", "cashier_entry_status", "source_ref", "comment",
                    ),
                    limit=40,
                    order_by=("id", "payment_date"),
                ),
            )

        show_rows(
            "Service orders (latest first):",
            select_rows(
                conn,
                "service_orders",
                (
                    "id", "order_number", "apartment_id", "apartment_number",
                    "service_item_code", "service_name_snapshot", "workflow_profile_code",
                    "order_status", "payment_status", "fulfillment_status", "requested_at",
                ),
                limit=60,
                order_by=("id", "requested_at"),
            ),
        )

        show_rows(
            "Service-order steps:",
            select_rows(
                conn,
                "service_order_steps",
                (
                    "id", "service_order_id", "step_code", "step_name",
                    "sequence_no", "is_required", "step_status",
                    "confirmed_at", "confirmed_by",
                ),
                limit=200,
                order_by=("id",),
            ),
        )

        show_rows(
            "Payment links:",
            select_rows(
                conn,
                "service_order_payment_links",
                (
                    "id", "service_order_id", "payment_id", "amount",
                    "linked_at", "linked_by", "note",
                ),
                limit=100,
                order_by=("id",),
            ),
        )

        show_rows(
            "Legacy remote requests:",
            select_rows(
                conn,
                "remote_requests",
                (
                    "id", "apartment_id", "apartment_number", "request_type",
                    "status", "created_at", "updated_at", "comment",
                ),
                limit=60,
                order_by=("id", "created_at"),
            ),
        )

        show_rows(
            "Staff principals:",
            select_rows(
                conn,
                "staff_principals",
                (
                    "id", "telegram_user_id", "user_id", "display_name",
                    "full_name", "is_active", "status",
                ),
                limit=200,
                order_by=("id",),
            ),
        )

        show_rows(
            "User roles:",
            select_rows(
                conn,
                "access_user_roles",
                (
                    "id", "user_id", "telegram_user_id", "role_code", "role_id",
                    "scope_type", "scope_value", "is_active",
                ),
                limit=300,
                order_by=("id",),
            ),
        )

        show_rows(
            "Direct user permissions:",
            select_rows(
                conn,
                "access_user_permissions",
                (
                    "id", "user_id", "telegram_user_id", "resource", "action",
                    "permission_code", "scope_type", "scope_value", "is_active",
                ),
                limit=500,
                order_by=("id",),
            ),
        )

        show_rows(
            "Role permissions:",
            select_rows(
                conn,
                "access_role_permissions",
                (
                    "id", "role_id", "role_code", "resource", "action",
                    "permission_code", "scope_type", "scope_value", "is_active",
                ),
                limit=500,
                order_by=("id",),
            ),
        )

        say()
        say("What the report will tell us:")
        say("  1) Whether the runtime-patched parking_bot imports and calls service_orders_workspace.")
        say("  2) Whether your sandbox contains the yesterday's reprogramming service order and its exact step.")
        say("  3) Whether the sandbox has payments.source_ref.")
        say("  4) Whether roles/permissions permit service_orders VIEW for REMOTE / ACCESS.")
    finally:
        conn.close()


def save_report() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = LOG_DIR / f"guard_sandbox_service_orders_diagnosis_v2_{stamp}.txt"
    report_path.write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    say("OSBB Guard Sandbox — Service Orders Diagnosis V2")
    separator()
    say(f"Project root: {ROOT}")
    say("This diagnostic is read-only.")

    inspect_bot_source()
    inspect_database()

    separator()
    say("Diagnosis completed. No DB or source code was changed.")
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as exc:  # noqa: BLE001
        say()
        separator("!")
        say(f"DIAGNOSIS FAILED: {type(exc).__name__}: {exc}")
        say(traceback.format_exc())
        exit_code = 1

    report = save_report()
    print()
    print("Report saved to:", report)
    input("\nPress Enter to close...")
    raise SystemExit(exit_code)
