"""
Найти Telegram ID, привязанный к квартире, в указанной sandbox-БД.

Скрипт только читает .db внутри Data\db\sandbox. Он не меняет базу,
бота или права.

Пример:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\find_sandbox_telegram_id.py ^
  --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09_guard_check_2026-06-26_12-56-09.db" ^
  --apartment 174
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"


def table_exists(cur: sqlite3.Cursor, name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    )
    return cur.fetchone() is not None


def columns(cur: sqlite3.Cursor, table: str) -> set[str]:
    if not table_exists(cur, table):
        return set()
    cur.execute(f'PRAGMA table_info("{table}")')
    return {row[1] for row in cur.fetchall()}


def safe_expr(cols: set[str], name: str, alias: str) -> str:
    return f"{alias}.{name}" if name in cols else f"NULL AS {name}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", required=True)
    parser.add_argument("--apartment", required=True)
    args = parser.parse_args()

    db = Path(args.sandbox).resolve()
    try:
        db.relative_to(SANDBOX_DIR.resolve())
    except ValueError:
        raise SystemExit("Разрешены только базы внутри Data\\db\\sandbox.")
    if not db.exists():
        raise SystemExit(f"Не найдена sandbox-БД: {db}")

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        if not table_exists(cur, "resident_accounts"):
            raise SystemExit("В БД нет resident_accounts.")
        if not table_exists(cur, "apartments"):
            raise SystemExit("В БД нет apartments.")

        rcols = columns(cur, "resident_accounts")
        acols = columns(cur, "apartments")

        if "telegram_user_id" not in rcols:
            raise SystemExit("В resident_accounts нет telegram_user_id.")

        account_unit_join = ""
        apartment_filter = ""
        params: list[str] = []

        if "apartment_id" in rcols and "id" in acols:
            account_unit_join = "LEFT JOIN apartments a ON a.id = r.apartment_id"
            if "apartment_number" in acols:
                apartment_filter = "CAST(a.apartment_number AS TEXT) = ?"
                params.append(str(args.apartment).strip())
        elif "apartment_number" in rcols:
            account_unit_join = "LEFT JOIN apartments a ON CAST(a.apartment_number AS TEXT) = CAST(r.apartment_number AS TEXT)"
            apartment_filter = "CAST(r.apartment_number AS TEXT) = ?"
            params.append(str(args.apartment).strip())
        else:
            raise SystemExit(
                "Не найдена понятная привязка resident_accounts к квартире."
            )

        if not apartment_filter:
            raise SystemExit("В apartments нет apartment_number.")

        fields = [
            "r.telegram_user_id AS telegram_user_id",
            safe_expr(rcols, "telegram_username", "r"),
            safe_expr(rcols, "telegram_first_name", "r"),
            safe_expr(rcols, "telegram_last_name", "r"),
            safe_expr(rcols, "status", "r"),
            (
                "a.apartment_number AS apartment_number"
                if "apartment_number" in acols
                else "NULL AS apartment_number"
            ),
        ]
        cur.execute(
            f"""
            SELECT {', '.join(fields)}
            FROM resident_accounts r
            {account_unit_join}
            WHERE {apartment_filter}
            ORDER BY r.telegram_user_id
            """,
            tuple(params),
        )
        rows = [dict(row) for row in cur.fetchall()]

        print("=" * 96)
        print("SANDBOX TELEGRAM ACCOUNT LOOKUP — READ ONLY")
        print("=" * 96)
        print("DB:", db)
        print("Apartment:", args.apartment)
        print()

        if not rows:
            print("Связанных Telegram-аккаунтов не найдено.")
            return 0

        for row in rows:
            display = " ".join(
                part for part in [
                    str(row.get("telegram_first_name") or "").strip(),
                    str(row.get("telegram_last_name") or "").strip(),
                ] if part
            ) or "-"
            print(f"Telegram ID: {row.get('telegram_user_id')}")
            print(f"Name: {display}")
            print(f"Username: {row.get('telegram_username') or '-'}")
            print(f"Status: {row.get('status') or '-'}")
            print(f"Apartment: {row.get('apartment_number') or args.apartment}")
            print("-" * 40)

        print("RESULT: READ-ONLY LOOKUP COMPLETED")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
