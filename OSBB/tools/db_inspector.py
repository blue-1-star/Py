#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = PROJECT_ROOT / "Data" / "db" / "osbb_test.db"


def connect(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    return con


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def header(title: str) -> None:
    print("=" * 90)
    print(title)
    print("=" * 90)


def section(title: str) -> None:
    print()
    print("-" * 90)
    print(title)
    print("-" * 90)


def table_names(con: sqlite3.Connection) -> list[str]:
    return [r["name"] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )]


def table_exists(con: sqlite3.Connection, table: str) -> bool:
    return con.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone() is not None


def columns(con: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    return con.execute(f"PRAGMA table_info({q(table)})").fetchall()


def column_names(con: sqlite3.Connection, table: str) -> list[str]:
    return [r["name"] for r in columns(con, table)]


def row_count(con: sqlite3.Connection, table: str) -> int | None:
    if not table_exists(con, table):
        return None
    return int(con.execute(f"SELECT COUNT(*) AS n FROM {q(table)}").fetchone()["n"])


def print_rows(rows: Iterable[sqlite3.Row], limit: int = 50) -> None:
    count = 0
    for row in rows:
        print(dict(row))
        count += 1
        if count >= limit:
            break
    if count == 0:
        print("(no rows)")


def list_tables(con: sqlite3.Connection, pattern: str | None = None) -> None:
    names = table_names(con)
    if pattern:
        p = pattern.lower()
        names = [name for name in names if p in name.lower()]
    for name in names:
        print(name)


def show_schema(con: sqlite3.Connection, table: str) -> None:
    if not table_exists(con, table):
        print(f"Table not found: {table}")
        return
    header(f"Schema: {table}")
    for col in columns(con, table):
        print(dict(col))


def show_admins(con: sqlite3.Connection) -> None:
    header("OSBB admins")
    if not table_exists(con, "bot_admins"):
        print("Table bot_admins not found.")
        return
    print_rows(con.execute("SELECT * FROM bot_admins ORDER BY id").fetchall())


def matching_tables(con: sqlite3.Connection, title: str, keywords: list[str]) -> None:
    header(title)
    names = [
        name for name in table_names(con)
        if any(k.lower() in name.lower() for k in keywords)
    ]
    if not names:
        print("(no matching tables)")
        return
    for name in names:
        print(f"{name:45s} rows={row_count(con, name)}")


def show_service_orders(con: sqlite3.Connection) -> None:
    header("Service Orders")
    for table in [
        "service_orders",
        "service_order_steps",
        "service_order_payment_links",
        "remote_assets",
        "remote_requests",
    ]:
        n = row_count(con, table)
        print(f"{table:35s} {'MISSING' if n is None else 'rows=' + str(n)}")
    if table_exists(con, "service_orders"):
        section("Last service_orders")
        cols = column_names(con, "service_orders")
        order_col = "id" if "id" in cols else cols[0]
        print_rows(con.execute(
            f"SELECT * FROM service_orders ORDER BY {q(order_col)} DESC LIMIT 20"
        ).fetchall())


def show_cashier(con: sqlite3.Connection) -> None:
    matching_tables(con, "Cashier / payment tables", ["cash", "payment", "receipt"])
    if table_exists(con, "payments"):
        section("payments schema compatibility")
        cols = column_names(con, "payments")
        for needed in ["source_ref", "source_type", "amount", "created_at"]:
            print(f"payments.{needed:20s} {'YES' if needed in cols else 'NO'}")
        section("Last payments")
        order_col = "id" if "id" in cols else cols[0]
        print_rows(con.execute(
            f"SELECT * FROM payments ORDER BY {q(order_col)} DESC LIMIT 20"
        ).fetchall())


def show_remotes(con: sqlite3.Connection) -> None:
    matching_tables(con, "Remote / access tables", ["remote", "barrier", "access"])
    for table in ["remote_assets", "remote_requests"]:
        if table_exists(con, table):
            section(f"Last {table}")
            cols = column_names(con, table)
            order_col = "id" if "id" in cols else cols[0]
            print_rows(con.execute(
                f"SELECT * FROM {q(table)} ORDER BY {q(order_col)} DESC LIMIT 20"
            ).fetchall())


def show_vehicles(con: sqlite3.Connection) -> None:
    matching_tables(con, "Vehicle / parking tables", ["vehicle", "car", "parking", "auto"])
    for table in table_names(con):
        low = table.lower()
        if any(k in low for k in ["vehicle", "parking", "auto", "car"]):
            section(f"Sample {table}")
            print_rows(con.execute(f"SELECT * FROM {q(table)} LIMIT 20").fetchall())


def show_roles(con: sqlite3.Connection) -> None:
    matching_tables(con, "Role / access tables", ["admin", "role", "permission", "guard", "operator", "access"])


def show_summary(con: sqlite3.Connection, db_path: Path) -> None:
    header("OSBB DATABASE INSPECTOR")
    print("Database:", db_path)
    print("Size KB :", round(db_path.stat().st_size / 1024, 1))

    section("Core table counts")
    for table in [
        "bot_admins",
        "residents",
        "apartments",
        "units",
        "vehicles",
        "vehicle_registry",
        "payments",
        "service_orders",
        "service_order_steps",
        "service_order_payment_links",
        "remote_assets",
        "remote_requests",
    ]:
        n = row_count(con, table)
        if n is not None:
            print(f"{table:35s} {n}")

    section("Schema compatibility")
    for table, col in [
        ("payments", "source_ref"),
        ("payments", "source_type"),
        ("service_orders", "id"),
        ("service_order_steps", "order_id"),
        ("remote_assets", "id"),
        ("bot_admins", "telegram_user_id"),
    ]:
        if not table_exists(con, table):
            print(f"{table}.{col:30s} TABLE MISSING")
        else:
            cols = column_names(con, table)
            print(f"{table}.{col:30s} {'YES' if col in cols else 'NO'}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Inspect OSBB SQLite database.")
    ap.add_argument("command", choices=[
        "summary", "tables", "schema", "admins", "roles",
        "cashier", "service-orders", "remotes", "vehicles", "search",
    ])
    ap.add_argument("arg", nargs="?", help="table name for schema, or search term")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DB path")
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = (PROJECT_ROOT / db_path).resolve()
    if not db_path.exists():
        raise SystemExit(f"DB not found: {db_path}")

    con = connect(db_path)
    try:
        if args.command == "summary":
            show_summary(con, db_path)
        elif args.command == "tables":
            list_tables(con)
        elif args.command == "schema":
            if not args.arg:
                raise SystemExit("schema requires table name")
            show_schema(con, args.arg)
        elif args.command == "admins":
            show_admins(con)
        elif args.command == "roles":
            show_roles(con)
        elif args.command == "cashier":
            show_cashier(con)
        elif args.command == "service-orders":
            show_service_orders(con)
        elif args.command == "remotes":
            show_remotes(con)
        elif args.command == "vehicles":
            show_vehicles(con)
        elif args.command == "search":
            if not args.arg:
                raise SystemExit("search requires term")
            list_tables(con, args.arg)
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
