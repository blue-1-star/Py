r"""
Диагностика начислений для sandbox-версии «Касса и платежи v2».

Только читает указанную sandbox-БД.
Ничего не меняет.

Показывает:
- реальную структуру charges и payment_allocations;
- начисления квартиры 174;
- доступные периоды и service_code;
- как квартира 174 связана с подъездом;
- есть ли начисления для подъезда 4.

Запуск:
g:\Programming\Py\venv\Scripts\python.exe G:\Programming\Py\OSBB\diagnose_sandbox_charges.py --sandbox "G:\Programming\Py\OSBB\Data\db\sandbox\osbb_test_cashier_v2_compat_check_2026-06-25_19-47-09.db"
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SANDBOX_DIR = ROOT / "Data" / "db" / "sandbox"


def table_exists(cur: sqlite3.Cursor, table: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None


def columns(cur: sqlite3.Cursor, table: str) -> list[str]:
    if not table_exists(cur, table):
        return []
    cur.execute(f'PRAGMA table_info("{table}")')
    return [row[1] for row in cur.fetchall()]


def print_rows(title: str, rows: list[sqlite3.Row], limit: int = 30) -> None:
    print()
    print(title)
    print("-" * len(title))
    if not rows:
        print("(нет строк)")
        return
    for row in rows[:limit]:
        print(dict(row))
    if len(rows) > limit:
        print(f"... показано {limit} из {len(rows)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", required=True)
    args = parser.parse_args()

    sandbox = Path(args.sandbox).resolve()
    try:
        sandbox.relative_to(SANDBOX_DIR.resolve())
    except ValueError:
        raise SystemExit("Разрешены только БД внутри Data\\db\\sandbox.")
    if not sandbox.exists():
        raise SystemExit(f"Не найдена sandbox-БД: {sandbox}")

    conn = sqlite3.connect(sandbox)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        print("=" * 100)
        print("SANDBOX CHARGES DIAGNOSTIC — READ ONLY")
        print("=" * 100)
        print("DB:", sandbox)

        for table in ("charges", "payment_allocations", "apartments", "service_items", "service_catalog"):
            print()
            print(f"{table}:")
            print("  columns:", ", ".join(columns(cur, table)) or "<нет таблицы>")
            if table_exists(cur, table):
                cur.execute(f'SELECT COUNT(*) AS n FROM "{table}"')
                print("  rows:", cur.fetchone()["n"])

        ccols = set(columns(cur, "charges"))
        acols = set(columns(cur, "apartments"))

        if not ccols:
            return 1

        # Find apartment 174 by old/new schema.
        if "apartment_number" in acols:
            cur.execute(
                """
                SELECT *
                FROM apartments
                WHERE CAST(apartment_number AS TEXT) = '174'
                """
            )
            print_rows("Квартира 174 в apartments", cur.fetchall())

        # Charges actually present for apartment 174.
        if "apartment_number" in ccols:
            cur.execute(
                """
                SELECT *
                FROM charges
                WHERE CAST(apartment_number AS TEXT) = '174'
                ORDER BY id DESC
                """
            )
            print_rows("Все строки charges для квартиры 174", cur.fetchall())

        if "apartment_id" in ccols and "apartment_number" in acols:
            cur.execute(
                """
                SELECT c.*
                FROM charges c
                JOIN apartments a ON a.id = c.apartment_id
                WHERE CAST(a.apartment_number AS TEXT) = '174'
                ORDER BY c.id DESC
                """
            )
            print_rows("Все строки charges для квартиры 174 через apartment_id", cur.fetchall())

        # Distinct periods/services showing real code values.
        if "period_code" in ccols:
            cur.execute(
                "SELECT DISTINCT period_code FROM charges ORDER BY period_code DESC LIMIT 40"
            )
            print_rows("Периоды, реально встречающиеся в charges", cur.fetchall())

        if "service_code" in ccols:
            cur.execute(
                """
                SELECT service_code, COUNT(*) AS n
                FROM charges
                GROUP BY service_code
                ORDER BY n DESC, service_code
                LIMIT 60
                """
            )
            print_rows("service_code, реально встречающиеся в charges", cur.fetchall())

        # Show only candidate July / parking-related rows if columns exist.
        conditions = []
        params = []
        if "period_code" in ccols:
            conditions.append("CAST(period_code AS TEXT) LIKE ?")
            params.append("%2026-07%")
        if "service_code" in ccols:
            conditions.append("LOWER(CAST(service_code AS TEXT)) LIKE ?")
            params.append("%park%")
        if conditions:
            cur.execute(
                f"""
                SELECT *
                FROM charges
                WHERE {' OR '.join(conditions)}
                ORDER BY id DESC
                LIMIT 100
                """,
                tuple(params),
            )
            print_rows("Кандидаты: июль 2026 ИЛИ parking", cur.fetchall(), limit=100)

        # Entrance 4 mapping and charges joined by apartment_number where possible.
        entrance_col = "entrance_number" if "entrance_number" in acols else (
            "entrance" if "entrance" in acols else None
        )
        if entrance_col and "apartment_number" in acols:
            cur.execute(
                f"""
                SELECT id, apartment_number, {entrance_col} AS entrance
                FROM apartments
                WHERE CAST({entrance_col} AS TEXT) = '4'
                ORDER BY apartment_number
                """
            )
            print_rows("Физические квартиры подъезда 4", cur.fetchall(), limit=300)

            if "apartment_number" in ccols:
                cur.execute(
                    f"""
                    SELECT c.*
                    FROM charges c
                    JOIN apartments a
                      ON CAST(a.apartment_number AS TEXT) =
                         CAST(c.apartment_number AS TEXT)
                    WHERE CAST(a.{entrance_col} AS TEXT) = '4'
                    ORDER BY c.id DESC
                    LIMIT 100
                    """
                )
                print_rows("Начисления, привязанные к подъезду 4", cur.fetchall(), limit=100)

        print()
        print("RESULT: READ-ONLY DIAGNOSTIC COMPLETED")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
