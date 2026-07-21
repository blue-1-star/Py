# -*- coding: utf-8 -*-
r"""
OSBB — read-only diagnosis of the Guard Sandbox bot and service orders.

Put this file directly into:
    G:\Programming\Py\OSBB\

It reads the sandbox path from:
    Start_OSBB_Guard_Sandbox_Bot_v2.bat

It DOES NOT modify:
- the sandbox database;
- osbb.db;
- parking_bot.py;
- config.py;
- any patcher or handler.

It creates only a textual report in:
    Data\db\logs\
"""

from __future__ import annotations

import importlib.util
import re
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
LOG_DIR = ROOT / "Data" / "db" / "logs"

LAUNCHER_BAT = ROOT / "Start_OSBB_Guard_Sandbox_Bot_v2.bat"
RUNNER = ROOT / "run_bot_guard_sandbox_v3.py"
PARKING_BOT = BOTS_DIR / "parking_bot.py"
WORKSPACE = BOTS_DIR / "handlers" / "service_orders_workspace.py"
V2_SWITCHER = ROOT / "switch_parking_bot_to_cashier_v2.py"
GUARD_PATCHER = ROOT / "patch_parking_bot_guard_workspace_v4.py"

REPORT: list[str] = []


def say(value: object = "") -> None:
    line = str(value)
    print(line)
    REPORT.append(line)


def line(char: str = "=") -> None:
    say(char * 100)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1251", "cp866"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Unable to decode text file: {path}")


def quote(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def extract_sandbox_path() -> Path:
    if not LAUNCHER_BAT.is_file():
        raise FileNotFoundError(
            "Launcher BAT not found:\n"
            f"  {LAUNCHER_BAT}\n"
            "Put this diagnosis script directly into G:\\Programming\\Py\\OSBB\\."
        )

    content = read_text(LAUNCHER_BAT)
    match = re.search(
        r'(?im)^\s*set\s+"SANDBOX=(.*?)"\s*$',
        content,
    )
    if not match:
        raise RuntimeError(
            "Could not find the SANDBOX= line in "
            f"{LAUNCHER_BAT.name}."
        )

    raw_path = match.group(1).strip()
    # The current launcher uses an absolute G:\... path. A variable here would
    # be intentionally refused instead of resolving it incorrectly.
    if "%" in raw_path:
        raise RuntimeError(
            "The sandbox path contains an environment variable and cannot be "
            f"resolved safely: {raw_path}"
        )
    return Path(raw_path)


def sqlite_connect_readonly(db_path: Path) -> sqlite3.Connection:
    # POSIX form works for file: SQLite URI on Windows as well.
    uri = "file:" + db_path.resolve().as_posix() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (name,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, name: str) -> list[str]:
    if not table_exists(conn, name):
        return []
    rows = conn.execute(f"PRAGMA table_info({quote(name)})").fetchall()
    return [str(row["name"]) for row in rows]


def count_rows(conn: sqlite3.Connection, name: str) -> int | None:
    if not table_exists(conn, name):
        return None
    return int(conn.execute(f"SELECT COUNT(*) FROM {quote(name)}").fetchone()[0])


def select_existing_columns(
    conn: sqlite3.Connection,
    table: str,
    desired: Iterable[str],
    *,
    limit: int = 20,
    order_candidates: Iterable[str] = ("id",),
) -> list[dict[str, Any]]:
    columns = table_columns(conn, table)
    if not columns:
        return []

    selected = [name for name in desired if name in columns]
    if not selected:
        selected = columns[: min(12, len(columns))]

    order_column = next((name for name in order_candidates if name in columns), None)
    sql = (
        "SELECT "
        + ", ".join(quote(name) for name in selected)
        + f" FROM {quote(table)}"
    )
    if order_column:
        sql += f" ORDER BY {quote(order_column)} DESC"
    sql += " LIMIT ?"
    rows = conn.execute(sql, (int(limit),)).fetchall()
    return [dict(row) for row in rows]


def print_rows(title: str, rows: list[dict[str, Any]]) -> None:
    say()
    say(title)
    if not rows:
        say("  (no rows)")
        return
    for row in rows:
        pairs = " | ".join(f"{key}={value!r}" for key, value in row.items())
        say("  " + pairs)


def line_numbers_with(source: str, needle: str, *, context: int = 2) -> list[str]:
    lines = source.splitlines()
    found: list[str] = []
    for idx, value in enumerate(lines):
        if needle.casefold() in value.casefold():
            start = max(0, idx - context)
            end = min(len(lines), idx + context + 1)
            fragment = "\n".join(
                f"{number + 1:>5}: {lines[number]}"
                for number in range(start, end)
            )
            found.append(fragment)
    return found


def load_patch_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Could not load patcher: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def inspect_runtime_source() -> None:
    line()
    say("BOT SOURCE AND IN-MEMORY PATCH CHECK")

    for path in (PARKING_BOT, V2_SWITCHER, GUARD_PATCHER, WORKSPACE, RUNNER):
        say(f"{'[OK]' if path.is_file() else '[MISSING]'} {path}")

    if not PARKING_BOT.is_file():
        return

    raw_source = read_text(PARKING_BOT)
    say()
    say(f"Raw parking_bot.py: {len(raw_source.splitlines())} lines")

    patched_source = None
    patch_messages: list[str] = []
    if V2_SWITCHER.is_file() and GUARD_PATCHER.is_file():
        try:
            v2 = load_patch_module(V2_SWITCHER, "_diagnosis_v2_switcher")
            guard = load_patch_module(GUARD_PATCHER, "_diagnosis_guard_patcher")
            patched_source, v2_changes = v2.patch(raw_source)
            patched_source, guard_changes = guard.patch(patched_source)
            compile(patched_source, str(PARKING_BOT), "exec")
            patch_messages.extend(
                [
                    "v2 patch: " + ("; ".join(v2_changes) if v2_changes else "(no reported changes)"),
                    "guard patch: " + ("; ".join(guard_changes) if guard_changes else "(no reported changes)"),
                    f"Patched parking_bot.py: {len(patched_source.splitlines())} lines; compile PASS",
                ]
            )
        except Exception as exc:  # diagnostic must continue with raw source
            patch_messages.append(f"PATCH ANALYSIS FAILED: {type(exc).__name__}: {exc}")
            patch_messages.append(traceback.format_exc())
    else:
        patch_messages.append("Patch analysis skipped because one or both patcher files are missing.")

    for message in patch_messages:
        say(message)

    checks = (
        "service_orders_workspace",
        "handle_service_orders_text",
        "show_service_operator_workspace",
        "🔑 Оператор услуг",
        "🔑 Заявки на пульты",
        "remote_requests",
        "guard_workspace",
    )

    for label, source in (
        ("RAW", raw_source),
        ("PATCHED", patched_source),
    ):
        say()
        say(f"{label} source integration markers:")
        if source is None:
            say("  (not available)")
            continue
        for marker in checks:
            matches = line_numbers_with(source, marker, context=1)
            say(f"  {marker!r}: {len(matches)} occurrence(s)")
            for block in matches[:4]:
                for fragment_line in block.splitlines():
                    say("    " + fragment_line)
                say("    ---")


def inspect_database(db_path: Path) -> None:
    line()
    say("SANDBOX DATABASE CHECK")
    say(f"Database: {db_path}")
    say(f"Exists: {db_path.is_file()}")
    if not db_path.is_file():
        return

    conn = sqlite_connect_readonly(db_path)
    try:
        say(f"Opened read-only: PASS")
        tables = [
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
        ]
        say()
        say("Relevant tables:")
        for name in tables:
            count = count_rows(conn, name)
            if count is None:
                say(f"  [MISSING] {name}")
            else:
                columns = ", ".join(table_columns(conn, name))
                say(f"  [OK] {name}: {count} row(s)")
                say(f"       columns: {columns}")

        if table_exists(conn, "payments"):
            payment_columns = set(table_columns(conn, "payments"))
            say()
            say(
                "payments.source_ref: "
                + ("PRESENT" if "source_ref" in payment_columns else "MISSING")
            )
            print_rows(
                "Latest payments:",
                select_existing_columns(
                    conn,
                    "payments",
                    (
                        "id", "payment_date", "apartment_id", "service_item_code",
                        "amount", "currency", "payment_method", "payment_channel",
                        "cashbox_code", "cashier_entry_status", "source_ref", "comment",
                    ),
                    limit=20,
                    order_candidates=("id", "payment_date"),
                ),
            )

        print_rows(
            "Latest service orders:",
            select_existing_columns(
                conn,
                "service_orders",
                (
                    "id", "order_number", "apartment_id", "apartment_number",
                    "service_item_code", "service_name_snapshot", "workflow_profile_code",
                    "order_status", "payment_status", "fulfillment_status", "requested_at",
                ),
                limit=30,
                order_candidates=("id", "requested_at"),
            ),
        )

        print_rows(
            "Latest service-order steps:",
            select_existing_columns(
                conn,
                "service_order_steps",
                (
                    "id", "service_order_id", "step_code", "step_name",
                    "sequence_no", "is_required", "step_status",
                    "confirmed_at", "confirmed_by",
                ),
                limit=100,
                order_candidates=("id", "service_order_id"),
            ),
        )

        print_rows(
            "Service-order payment links:",
            select_existing_columns(
                conn,
                "service_order_payment_links",
                (
                    "id", "service_order_id", "payment_id", "amount",
                    "linked_at", "linked_by", "note",
                ),
                limit=50,
                order_candidates=("id",),
            ),
        )

        print_rows(
            "Legacy remote requests:",
            select_existing_columns(
                conn,
                "remote_requests",
                (
                    "id", "apartment_id", "apartment_number", "request_type",
                    "status", "created_at", "updated_at", "comment",
                ),
                limit=30,
                order_candidates=("id", "created_at"),
            ),
        )

        print_rows(
            "Staff principals:",
            select_existing_columns(
                conn,
                "staff_principals",
                (
                    "id", "telegram_user_id", "user_id", "display_name",
                    "full_name", "is_active", "status",
                ),
                limit=100,
                order_candidates=("id",),
            ),
        )

        print_rows(
            "User roles:",
            select_existing_columns(
                conn,
                "access_user_roles",
                (
                    "id", "user_id", "telegram_user_id", "role_code",
                    "role_id", "is_active", "scope_type", "scope_value",
                ),
                limit=200,
                order_candidates=("id",),
            ),
        )

        print_rows(
            "Direct user permissions:",
            select_existing_columns(
                conn,
                "access_user_permissions",
                (
                    "id", "user_id", "telegram_user_id", "resource", "action",
                    "permission_code", "scope_type", "scope_value", "is_active",
                ),
                limit=300,
                order_candidates=("id",),
            ),
        )

        print_rows(
            "Role permissions:",
            select_existing_columns(
                conn,
                "access_role_permissions",
                (
                    "id", "role_id", "role_code", "resource", "action",
                    "permission_code", "scope_type", "scope_value", "is_active",
                ),
                limit=300,
                order_candidates=("id",),
            ),
        )

        say()
        say("Interpretation guide:")
        say("  - If 'service_orders_workspace' / 'handle_service_orders_text' is absent from PATCHED source,")
        say("    the sandbox bot cannot enter the new service-order interface.")
        say("  - If it is present, but the screen still falls back to old 'remote_requests',")
        say("    inspect roles/permissions for resource=service_orders, action=VIEW,")
        say("    scope_type=SERVICE_CATEGORY, scope_value=REMOTE or ACCESS.")
        say("  - If payments.source_ref is missing but the workspace file contains")
        say("    '_payments_has_source_ref', the source_ref crash is already neutralized.")
    finally:
        conn.close()


def write_report() -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = LOG_DIR / f"guard_sandbox_service_orders_diagnosis_{stamp}.txt"
    report_path.write_text("\n".join(REPORT) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    say("OSBB Guard Sandbox — Service Orders Diagnosis")
    line()
    say(f"Project root: {ROOT}")
    say(f"Launcher BAT: {LAUNCHER_BAT}")

    sandbox_db = extract_sandbox_path()
    say(f"Sandbox selected by BAT: {sandbox_db}")

    inspect_runtime_source()
    inspect_database(sandbox_db)

    line()
    say("Diagnosis completed. No database or source files were changed.")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as error:  # noqa: BLE001
        say()
        line("!")
        say(f"DIAGNOSIS FAILED: {type(error).__name__}: {error}")
        say(traceback.format_exc())
        code = 1

    report_file = write_report()
    print()
    print("Report written to:", report_file)
    input("\nPress Enter to close...")
    raise SystemExit(code)
