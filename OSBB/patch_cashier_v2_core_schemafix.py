r"""
Исправление schema-compatibility для cashier_v2_core.py.

Проблема:
В текущей БД таблица charges не имеет c.apartment_id.
Старый open_charges() правильно фильтровал по apartment_number, но потом
безусловно выбирал c.apartment_id — из-за этого падал сценарий «Бумажка».

Скрипт:
- по умолчанию ничего не меняет;
- собирает исправленную версию в памяти;
- при --sandbox выполняет безопасный SQL smoke-test на указанной sandbox-копии;
- при --apply создаёт backup cashier_v2_core.py и заменяет ТОЛЬКО функцию
  open_charges();
- не меняет базу данных и не меняет parking_bot.py.

Примеры:
Проверка исправления на sandbox:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\patch_cashier_v2_core_schemafix.py --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"

Применить код после успешной проверки:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\patch_cashier_v2_core_schemafix.py --apply
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import os
import re
import sqlite3
import sys
import traceback
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
BOTS_DIR = ROOT / "Bots"
CORE_FILE = ROOT / "cashier_v2_core.py"
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"

REPLACEMENT = '\ndef open_charges(\n    *,\n    apartment_id: int | None = None,\n    apartment_number: str | None = None,\n    entrance_number: str | None = None,\n    period_code: str | None = None,\n    service_code: str | None = None,\n    service_item_code: str | None = None,\n) -> list[dict]:\n    """\n    Return open charges using the schema actually present in the database.\n\n    Older OSBB billing tables identify a charge only by apartment_number;\n    newer ones may also have apartment_id.  This function supports both.\n    """\n    conn = get_conn()\n    try:\n        cur = conn.cursor()\n        if not table_exists(cur, "charges") or not table_exists(cur, "payment_allocations"):\n            return []\n\n        ccols = table_columns(cur, "charges")\n        acols = table_columns(cur, "apartments")\n        allocation_col = allocation_amount_column(cur)\n        if not allocation_col or "amount" not in ccols:\n            return []\n\n        has_charge_apartment_id = "apartment_id" in ccols\n        has_charge_apartment_number = "apartment_number" in ccols\n        has_apartment_number = "apartment_number" in acols\n\n        # Use apartments only when it is required for entrance filtering or\n        # to convert legacy charges(apartment_number) to a physical unit id.\n        join_sql = ""\n        joined_apartments = False\n        if has_charge_apartment_id:\n            if entrance_number:\n                join_sql = "LEFT JOIN apartments a ON a.id = c.apartment_id"\n                joined_apartments = True\n        elif has_charge_apartment_number and has_apartment_number:\n            join_sql = (\n                "LEFT JOIN apartments a "\n                "ON CAST(a.apartment_number AS TEXT) = "\n                "CAST(c.apartment_number AS TEXT)"\n            )\n            joined_apartments = True\n\n        filters: list[str] = []\n        params: list[Any] = []\n\n        # A physical unit is always required unless we are explicitly\n        # enumerating an entrance for a reviewed batch.\n        unit_filter_added = False\n        if apartment_id is not None:\n            if has_charge_apartment_id:\n                filters.append("c.apartment_id = ?")\n                params.append(int(apartment_id))\n                unit_filter_added = True\n            elif joined_apartments:\n                filters.append("a.id = ?")\n                params.append(int(apartment_id))\n                unit_filter_added = True\n\n        if not unit_filter_added and apartment_number:\n            if has_charge_apartment_number:\n                filters.append("CAST(c.apartment_number AS TEXT) = ?")\n                params.append(text(apartment_number))\n                unit_filter_added = True\n            elif joined_apartments and has_apartment_number:\n                filters.append("CAST(a.apartment_number AS TEXT) = ?")\n                params.append(text(apartment_number))\n                unit_filter_added = True\n\n        if entrance_number:\n            entrance_col = (\n                "entrance_number" if "entrance_number" in acols\n                else "entrance" if "entrance" in acols\n                else None\n            )\n            if not joined_apartments or not entrance_col:\n                return []\n            filters.append(f"CAST(a.{entrance_col} AS TEXT) = ?")\n            params.append(text(entrance_number))\n            unit_filter_added = True\n\n        if not unit_filter_added:\n            return []\n\n        if period_code and "period_code" in ccols:\n            filters.append("c.period_code = ?")\n            params.append(period_code)\n        if service_code and "service_code" in ccols:\n            filters.append("c.service_code = ?")\n            params.append(service_code)\n        if service_item_code and "service_item_code" in ccols:\n            filters.append("c.service_item_code = ?")\n            params.append(service_item_code)\n\n        status_sql = (\n            "AND COALESCE(c.charge_status, \'\') <> \'cancelled\'"\n            if "charge_status" in ccols\n            else (\n                "AND COALESCE(c.status, \'\') <> \'cancelled\'"\n                if "status" in ccols else ""\n            )\n        )\n\n        apartment_id_expr = (\n            "c.apartment_id"\n            if has_charge_apartment_id\n            else "a.id"\n            if joined_apartments\n            else "NULL"\n        )\n        apartment_number_expr = (\n            "COALESCE(a.apartment_number, c.apartment_number)"\n            if joined_apartments and has_charge_apartment_number\n            else "c.apartment_number"\n            if has_charge_apartment_number\n            else "a.apartment_number"\n            if joined_apartments and has_apartment_number\n            else "NULL"\n        )\n        period_expr = "c.period_code" if "period_code" in ccols else "NULL"\n        service_expr = "c.service_code" if "service_code" in ccols else "NULL"\n        item_expr = "c.service_item_code" if "service_item_code" in ccols else "NULL"\n\n        cur.execute(\n            f"""\n            SELECT\n                c.id AS charge_id,\n                {apartment_id_expr} AS apartment_id,\n                {apartment_number_expr} AS apartment_number,\n                {period_expr} AS period_code,\n                {service_expr} AS service_code,\n                {item_expr} AS service_item_code,\n                c.amount AS charge_amount,\n                COALESCE(SUM(pa.{allocation_col}), 0) AS allocated_amount\n            FROM charges c\n            {join_sql}\n            LEFT JOIN payment_allocations pa ON pa.charge_id = c.id\n            WHERE {\' AND \'.join(filters)}\n            {status_sql}\n            GROUP BY c.id\n            HAVING c.amount - COALESCE(SUM(pa.{allocation_col}), 0) > 0.00001\n            ORDER BY COALESCE({apartment_number_expr}, \'\'), c.id\n            """,\n            tuple(params),\n        )\n\n        result = []\n        for row in cur.fetchall():\n            item = dict(row)\n            item["charge_amount"] = float(item["charge_amount"] or 0)\n            item["allocated_amount"] = float(item["allocated_amount"] or 0)\n            item["outstanding_amount"] = round(\n                max(0.0, item["charge_amount"] - item["allocated_amount"]),\n                2,\n            )\n            result.append(item)\n        return result\n    finally:\n        conn.close()\n'


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Не удалось подготовить модуль: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def patched_source(source: str) -> str:
    start = source.find("def open_charges(")
    end = source.find("\ndef suggested_charge(", start)
    if start < 0 or end < 0:
        raise RuntimeError(
            "В cashier_v2_core.py не найдена ожидаемая функция open_charges(). "
            "Исходный файл не менялся."
        )
    old = source[start:end]
    if "c.apartment_id AS apartment_id" not in old:
        raise RuntimeError(
            "Исходная функция уже отличается от ожидаемой версии. "
            "Исходный файл не менялся."
        )
    return source[:start] + REPLACEMENT.rstrip() + "\n\n" + source[end + 1:]


def clone_paths(original, sandbox: Path):
    try:
        cloned = copy.copy(original)
        if cloned is original:
            raise RuntimeError
    except Exception:
        data = {}
        for name in dir(original):
            if name.startswith("_"):
                continue
            value = getattr(original, name)
            if not callable(value):
                data[name] = value
        cloned = SimpleNamespace(**data)
    try:
        setattr(cloned, "OSBB_TEST_DB_FILE", sandbox)
    except Exception:
        object.__setattr__(cloned, "OSBB_TEST_DB_FILE", sandbox)
    return cloned


def ensure_sandbox(path: Path) -> Path:
    path = path.resolve()
    try:
        path.relative_to(SANDBOX_DIR.resolve())
    except ValueError as exc:
        raise ValueError(
            "Можно проверять только БД в Data\\db\\sandbox."
        ) from exc
    return path


def smoke_test(source: str, sandbox: Path) -> tuple[int, int]:
    for folder in (ROOT, BOTS_DIR, ROOT.parent):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))

    import config
    config.paths = clone_paths(config.paths, sandbox)
    config.USE_TEST_DB = True
    os.environ["OSBB_SANDBOX_DB"] = str(sandbox)
    os.environ["OSBB_SANDBOX_MODE"] = "1"

    # prevent a previously loaded live module from being reused
    for module_name in [
        "cashier_v2_core_schemafix_smoke",
        "cashier_v2_core",
        "handlers.cashier_operator",
        "db_access",
        "audit_logger",
    ]:
        sys.modules.pop(module_name, None)

    module = type(sys)("cashier_v2_core_schemafix_smoke")
    module.__file__ = str(CORE_FILE)
    sys.modules[module.__name__] = module
    exec(compile(source, str(CORE_FILE), "exec"), module.__dict__)

    # The exact failing route was unit 174 / 2026-07 / PARKING_DAY.
    single = module.open_charges(
        apartment_number="174",
        period_code="2026-07",
        service_code="PARKING_DAY",
    )
    # Batch route should also be schema-safe even when legacy charges only
    # have apartment_number and no apartment_id.
    batch = module.open_charges(
        entrance_number="4",
        period_code="2026-07",
        service_code="PARKING_DAY",
    )
    return len(single), len(batch)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", help="Путь к .db внутри Data\\db\\sandbox")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    print("=" * 100)
    print("CASHIER V2 CORE SCHEMA FIX")
    print("=" * 100)
    print("Core:", CORE_FILE)
    print("Apply:", args.apply)

    if not CORE_FILE.exists():
        raise SystemExit(f"Не найден файл: {CORE_FILE}")

    original = CORE_FILE.read_text(encoding="utf-8")
    try:
        fixed = patched_source(original)
        compile(fixed, str(CORE_FILE), "exec")
        print("Code patch: OK (compiled in memory)")
    except Exception as exc:
        print("Code patch: FAILED")
        print(exc)
        return 1

    if args.sandbox:
        try:
            sandbox = ensure_sandbox(Path(args.sandbox))
            if not sandbox.exists():
                raise FileNotFoundError(f"Не найдена sandbox-БД: {sandbox}")
            one, batch = smoke_test(fixed, sandbox)
            print("Sandbox SQL smoke-test: OK")
            print("  open charges for apartment 174:", one)
            print("  open charges for entrance 4:", batch)
        except Exception:
            print("Sandbox SQL smoke-test: FAILED")
            traceback.print_exc()
            return 1

    if not args.apply:
        print("DRY RUN COMPLETED - NO FILES AND NO DATABASES WERE CHANGED")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup = CORE_FILE.with_name(
        f"{CORE_FILE.stem}_before_schemafix_{stamp}{CORE_FILE.suffix}"
    )
    backup.write_text(original, encoding="utf-8")
    CORE_FILE.write_text(fixed, encoding="utf-8")
    print("APPLIED")
    print("Backup:", backup)
    print("Updated:", CORE_FILE)
    print("No database was modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
