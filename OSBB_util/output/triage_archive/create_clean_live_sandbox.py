r"""
Создание следующей чистой sandbox-копии для живого теста.

Источник:
  Data\db\osbb_test.db
  (основная тестовая база проекта, не текущая guard sandbox с квитанциями R2...)

Что делает:
- проверяет, что в базовой тестовой БД нет записей прежнего cashier/guard/service
  теста; если они есть, останавливается и ничего не копирует;
- создаёт новую .db внутри Data\db\sandbox;
- применяет к НОВОЙ КОПИИ:
    1) базовую кассу O/K1–K6/C/BANK;
    2) cashier v2 compatibility;
    3) роли и кабинет охраны;
    4) общий контур заказов услуг/пультов/телефонного доступа;
- по желанию назначает указанному Telegram ID роль GUARD_O только в этой новой
  sandbox-копии;
- создаёт отдельный .bat для запуска именно этой новой копии.

Исходная osbb_test.db, рабочая osbb.db, существующие sandbox-копии и
parking_bot.py не меняются.

Пример:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\create_clean_live_sandbox.py --guard-user 210312208
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parent
BOTS = ROOT / "Bots"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"

for folder in (ROOT, BOTS, ROOT.parent):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

import config


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось подготовить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def copy_database(source: Path, target: Path) -> None:
    src = sqlite3.connect(f"file:{source.as_posix()}?mode=ro", uri=True)
    try:
        dst = sqlite3.connect(target)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()


def table_exists(cur: sqlite3.Cursor, name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    )
    return cur.fetchone() is not None


def row_count(cur: sqlite3.Cursor, name: str) -> int:
    if not table_exists(cur, name):
        return 0
    cur.execute(f'SELECT COUNT(*) FROM "{name}"')
    return int(cur.fetchone()[0] or 0)


def base_workflow_counts(base: Path) -> dict[str, int]:
    names = [
        "cashier_receipts",
        "cashbox_operations",
        "payment_notices",
        "cashier_batches",
        "cashier_batch_items",
        "remote_handover_events",
        "service_orders",
        "remote_assets",
        "service_access_credentials",
    ]
    conn = sqlite3.connect(f"file:{base.as_posix()}?mode=ro", uri=True)
    try:
        cur = conn.cursor()
        return {name: row_count(cur, name) for name in names}
    finally:
        conn.close()


def ensure_cashier_base(conn: sqlite3.Connection, migration) -> dict[str, Any]:
    cur = conn.cursor()
    migration.ensure_cashboxes_table(cur)
    migration.ensure_cashbox_operations_table(cur)
    receipts_added = migration.ensure_cashier_receipts(cur)
    links_added = migration.ensure_link_columns(cur)

    boxes = []
    for code, name, active, comment in migration.CASHBOXES:
        boxes.append(
            f"{code}:{migration.upsert_cashbox(cur, code, name, active, comment)}"
        )

    boxes.append(
        "K:"
        + migration.upsert_cashbox(
            cur,
            "K",
            "K — агрегат консьержей (только история/отчёт)",
            0,
            "Не точка приёма. Новые операции вводить в K1–K6.",
        )
    )

    indexes: list[str] = []
    index_defs = [
        (
            "idx_cashier_receipts_status",
            "CREATE INDEX idx_cashier_receipts_status ON cashier_receipts(entry_status, receipt_date, id)",
        ),
        (
            "idx_cashier_receipts_cashbox",
            "CREATE INDEX idx_cashier_receipts_cashbox ON cashier_receipts(cashbox_code, receipt_date)",
        ),
        (
            "idx_cashier_receipts_apartment",
            "CREATE INDEX idx_cashier_receipts_apartment ON cashier_receipts(apartment_id, apartment_number, period_code)",
        ),
        (
            "idx_cashier_receipts_allocation",
            "CREATE INDEX idx_cashier_receipts_allocation ON cashier_receipts(allocation_status, entry_status)",
        ),
    ]
    if table_exists(cur, "payments"):
        index_defs.append(
            (
                "idx_payments_cashier_receipt",
                "CREATE INDEX idx_payments_cashier_receipt ON payments(cashier_receipt_id)",
            )
        )
    index_defs.extend(
        [
            (
                "idx_cashbox_operations_cashier_receipt",
                "CREATE INDEX idx_cashbox_operations_cashier_receipt ON cashbox_operations(cashier_receipt_id)",
            ),
            (
                "idx_cashbox_operations_transfer_group",
                "CREATE INDEX idx_cashbox_operations_transfer_group ON cashbox_operations(transfer_group_ref)",
            ),
        ]
    )
    for name, sql in index_defs:
        if migration.create_index_if_missing(cur, name, sql):
            indexes.append(name)

    balances = {}
    cur.execute("SELECT cashbox_code FROM cashboxes ORDER BY cashbox_code")
    for (code,) in cur.fetchall():
        balances[code] = migration.recalc_balance(cur, code)

    return {
        "cashboxes": boxes,
        "receipts_added": receipts_added,
        "links_added": links_added,
        "indexes": indexes,
        "balances": balances,
    }


def grant_guard_role(
    conn: sqlite3.Connection,
    telegram_id: str,
    display_name: str | None,
) -> None:
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        """
        INSERT INTO staff_principals (
            telegram_user_id, display_name, is_active, note, created_at, updated_at
        )
        VALUES (?, ?, 1, ?, ?, ?)
        ON CONFLICT(telegram_user_id) DO UPDATE SET
            display_name = COALESCE(excluded.display_name, staff_principals.display_name),
            is_active = 1,
            note = excluded.note,
            updated_at = excluded.updated_at
        """,
        (
            str(telegram_id),
            display_name or None,
            "Автоматическое назначение только в новой clean sandbox.",
            now,
            now,
        ),
    )
    cur.execute(
        """
        INSERT INTO access_user_roles (
            telegram_user_id, role_code, scope_type, scope_value,
            is_active, granted_by, note, created_at, updated_at
        )
        VALUES (?, 'GUARD_O', 'ALL', '*', 1,
                'CREATE_CLEAN_LIVE_SANDBOX',
                'Только для живого теста clean sandbox.', ?, ?)
        ON CONFLICT(telegram_user_id, role_code, scope_type, scope_value)
        DO UPDATE SET
            is_active = 1,
            granted_by = excluded.granted_by,
            note = excluded.note,
            updated_at = excluded.updated_at
        """,
        (str(telegram_id), now, now),
    )


def create_launcher(target_db: Path) -> Path:
    runner = ROOT / "run_bot_guard_sandbox_v3.py"
    launcher = ROOT / "Start_OSBB_Live_Service_Sandbox_Bot.bat"
    project = str(ROOT)
    python = r"G:\Programming\Py\venv\Scripts\python.exe"

    content = f"""@echo off
setlocal EnableExtensions

rem Создан автоматически: чистая live sandbox для услуг / пультов.
rem Остановить бота: Ctrl+C в этом отдельном окне.

set "PROJECT={project}"
set "PYTHON={python}"
set "RUNNER=%PROJECT%\\run_bot_guard_sandbox_v3.py"
set "SANDBOX={target_db}"

if not exist "%PYTHON%" (
    echo [ERROR] Не найден Python:
    echo %PYTHON%
    pause
    exit /b 1
)

if not exist "%RUNNER%" (
    echo [ERROR] Не найден launcher:
    echo %RUNNER%
    pause
    exit /b 1
)

if not exist "%SANDBOX%" (
    echo [ERROR] Не найдена clean sandbox:
    echo %SANDBOX%
    pause
    exit /b 1
)

echo Запускаю новую clean sandbox в отдельном окне.
echo Перед запуском остановите любой другой экземпляр Telegram-бота.
start "OSBB Live Service Sandbox" cmd.exe /k ""%PYTHON%" "%RUNNER%" --sandbox "%SANDBOX%" --run"

endlocal
"""
    launcher.write_text(content, encoding="utf-8-sig")
    return launcher


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--guard-user",
        help="Telegram ID тестового пользователя, которому выдать GUARD_O только в новой копии.",
    )
    parser.add_argument(
        "--guard-name",
        default="Тестовый охранник O",
        help="Отображаемое имя в staff_principals.",
    )
    parser.add_argument(
        "--allow-nonempty-base",
        action="store_true",
        help="Разрешить создание копии, даже если base osbb_test.db уже содержит workflow-записи.",
    )
    args = parser.parse_args()

    base = Path(config.paths.OSBB_TEST_DB_FILE).resolve()
    prod = Path(config.paths.OSBB_DB_FILE).resolve()
    if base == prod:
        raise SystemExit("ОТКАЗ: OSBB_TEST_DB_FILE указывает на рабочую БД.")
    if not base.exists():
        raise SystemExit(f"Не найдена базовая тестовая БД: {base}")

    # Base must be the normal test DB, never an existing sandbox.
    try:
        base.relative_to(SANDBOX_DIR.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit(
            "ОТКАЗ: базой должна быть osbb_test.db, а не старая sandbox-копия."
        )

    counts = base_workflow_counts(base)
    nonempty = {name: count for name, count in counts.items() if count > 0}
    if nonempty and not args.allow_nonempty_base:
        print("Базовая osbb_test.db уже содержит workflow-записи:")
        for name, count in nonempty.items():
            print(f"  {name}: {count}")
        print()
        print("Новая clean sandbox НЕ создана.")
        print(
            "Это защита от переноса старых тестовых операций в новую копию. "
            "Сначала выберите действительно чистую базу."
        )
        return 2

    required_files = {
        "cashier base": ROOT / "migrate_cashier_operator_editor.py",
        "cashier v2": ROOT / "migrate_cashier_v2_compat.py",
        "access": ROOT / "migrate_access_control_and_guard.py",
        "services": ROOT / "migrate_service_orders_and_fulfillment.py",
        "guard runner": ROOT / "run_bot_guard_sandbox_v3.py",
    }
    missing = [f"{label}: {path}" for label, path in required_files.items() if not path.exists()]
    if missing:
        print("Не найдены нужные файлы:")
        print("\n".join(missing))
        return 1

    stamp = now_stamp()
    target = SANDBOX_DIR / f"osbb_test_live_services_{stamp}.db"
    report = SANDBOX_DIR / f"clean_live_sandbox_{stamp}.txt"
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "=" * 100,
        "CLEAN LIVE SANDBOX CREATION",
        "=" * 100,
        f"Base test DB (read-only): {base}",
        f"New sandbox: {target}",
        f"Guard user: {args.guard_user or '(not assigned)'}",
        "",
        "Base workflow counts before copy:",
        *[f"  {name}: {count}" for name, count in counts.items()],
        "",
    ]

    try:
        copy_database(base, target)
        lines.extend(["1. Snapshot: OK", ""])

        cash_mig = load_module(required_files["cashier base"], "_clean_cashier_base")
        v2_mig = load_module(required_files["cashier v2"], "_clean_cashier_v2")
        access_mig = load_module(required_files["access"], "_clean_access")
        service_mig = load_module(required_files["services"], "_clean_services")

        conn = sqlite3.connect(target)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON")

            cash_result = ensure_cashier_base(conn, cash_mig)
            v2_result = v2_mig.ensure_cashier_v2_schema(conn)
            access_result = access_mig.ensure_access_schema(conn)
            service_result = service_mig.ensure_schema(conn)

            if args.guard_user:
                grant_guard_role(conn, str(args.guard_user), args.guard_name)

            conn.commit()

            cur = conn.cursor()
            output_counts = {
                name: row_count(cur, name)
                for name in [
                    "cashier_receipts",
                    "cashbox_operations",
                    "payment_notices",
                    "remote_handover_events",
                    "service_orders",
                    "remote_assets",
                    "service_access_credentials",
                ]
            }
            cur.execute(
                """
                SELECT COUNT(*)
                FROM access_user_roles
                WHERE telegram_user_id = ?
                  AND role_code = 'GUARD_O'
                  AND is_active = 1
                """,
                (str(args.guard_user or ""),),
            )
            guard_assignments = int(cur.fetchone()[0] or 0)
        finally:
            conn.close()

        launcher = create_launcher(target)

        lines.extend([
            "2. Cashier base: OK",
            f"   Cashboxes: {', '.join(cash_result['cashboxes'])}",
            f"   Cashbox balances: {cash_result['balances']}",
            "",
            "3. Cashier v2: OK",
            f"   {v2_result}",
            "",
            "4. Access / guard schema: OK",
            f"   {access_result}",
            "",
            "5. Service orders / remotes / phone access schema: OK",
            f"   {service_result}",
            "",
            "6. Clean workflow counts in the NEW sandbox:",
            *[f"   {name}: {count}" for name, count in output_counts.items()],
            f"   GUARD_O assignment for requested test user: {guard_assignments}",
            "",
            f"7. Launcher created: {launcher}",
            "",
            "RESULT: READY FOR LIVE SANDBOX TEST",
            "Base osbb_test.db and all previous sandbox copies were not modified.",
        ])
        code = 0
    except Exception:
        lines.extend([
            "RESULT: FAILED — NEW SANDBOX WAS NOT APPROVED FOR TEST",
            traceback.format_exc(),
        ])
        code = 1

    report.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("Report:", report)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
