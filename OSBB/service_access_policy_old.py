#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
service_access_policy.py

OSBB working module: service access policy v1.

Назначение:
  Единая read-only проверка доступности услуги для квартиры на основе:
  - service_catalog.access_policy_*
  - charges
  - payment_allocations

Этот модуль НЕ меняет БД.

Основная функция:

    result = check_service_allowed(conn, apartment_number, service_code)

Возвращает dict:

    {
        "allowed": bool,
        "decision": "ALLOW" | "WARN" | "BLOCK" | "ERROR",
        "service_code": "...",
        "service_name": "...",
        "apartment_number": "...",
        "policy": {...},
        "debt": {...},
        "message": "..."
    }

Режимы:
  NONE  -> ALLOW
  WARN  -> allowed=True, decision=WARN
  BLOCK -> allowed=False, decision=BLOCK

Scope v1:
  NONE
  PARKING
  ACCESS
  ALL_CASH_COLLECTABLE
  MANUAL
"""

from __future__ import annotations

import sqlite3
from typing import Any


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def money(value: Any) -> str:
    n = float(value or 0)
    if abs(n - round(n)) < 0.00001:
        return str(int(round(n)))
    return f"{n:.2f}"


def table_exists(cur: sqlite3.Cursor, table_name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cur.fetchone() is not None


def table_columns(cur: sqlite3.Cursor, table_name: str) -> set[str]:
    if not table_exists(cur, table_name):
        return set()
    cur.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cur.fetchall()}


def _row_to_dict(row: Any) -> dict[str, Any]:
    if row is None:
        return {}
    if isinstance(row, dict):
        return row
    try:
        return dict(row)
    except Exception:
        return {}


def _allocation_amount_column(cols: set[str]) -> str | None:
    if "amount" in cols:
        return "amount"
    if "allocated_amount" in cols:
        return "allocated_amount"
    return None


def service_scope_match(scope: str, service_code: Any) -> bool:
    scope = text(scope).upper()
    service = text(service_code).upper()

    if scope in ("", "NONE"):
        return False

    if scope == "PARKING":
        return service in {"PARKING_DAY", "PARKING_NIGHT"} or service.startswith("PARKING")

    if scope == "ACCESS":
        return "BARRIER" in service or "PHONE" in service or "REMOTE" in service

    if scope == "ALL_CASH_COLLECTABLE":
        return True

    if scope == "MANUAL":
        return False

    return False


def _charge_amount_expr(charge_cols: set[str]) -> str:
    if "net_amount" in charge_cols and "amount" in charge_cols:
        return "COALESCE(c.net_amount, c.amount, 0)"
    if "amount" in charge_cols:
        return "COALESCE(c.amount, 0)"
    if "net_amount" in charge_cols:
        return "COALESCE(c.net_amount, 0)"
    return "0"


def load_service_policy(conn: sqlite3.Connection, service_code: str) -> dict[str, Any] | None:
    cur = conn.cursor()
    if not table_exists(cur, "service_catalog"):
        return None

    cur.execute(
        "SELECT * FROM service_catalog WHERE service_code = ?",
        (text(service_code),),
    )
    row = cur.fetchone()
    return _row_to_dict(row) if row else None


def find_blocking_debt_rows(
    conn: sqlite3.Connection,
    apartment_number: Any,
    scope: str,
) -> list[dict[str, Any]]:
    """
    Read-only calculation of outstanding charge rows matching policy scope.
    """
    cur = conn.cursor()
    if not table_exists(cur, "charges"):
        return []

    charge_cols = table_columns(cur, "charges")
    if "apartment_number" not in charge_cols:
        return []

    service_expr = "COALESCE(c.service_code, '')" if "service_code" in charge_cols else "''"
    period_expr = "COALESCE(c.period_code, '')" if "period_code" in charge_cols else "''"

    status_filter = ""
    if "status" in charge_cols:
        status_filter = "AND COALESCE(c.status, '') <> 'cancelled'"
    elif "charge_status" in charge_cols:
        status_filter = "AND COALESCE(c.charge_status, '') <> 'cancelled'"

    allocation_join = ""
    allocation_select = "0 AS allocated_amount"
    if table_exists(cur, "payment_allocations"):
        alloc_cols = table_columns(cur, "payment_allocations")
        amount_col = _allocation_amount_column(alloc_cols)
        if amount_col and "charge_id" in alloc_cols:
            allocation_join = "LEFT JOIN payment_allocations pa ON pa.charge_id = c.id"
            allocation_select = f'COALESCE(SUM(pa."{amount_col}"), 0) AS allocated_amount'

    cur.execute(f"""
        SELECT
            c.id AS charge_id,
            {period_expr} AS period_code,
            {service_expr} AS service_code,
            {_charge_amount_expr(charge_cols)} AS amount,
            {allocation_select}
        FROM charges c
        {allocation_join}
        WHERE c.apartment_number = ?
        {status_filter}
        GROUP BY c.id
        ORDER BY {period_expr}, c.id
    """, (text(apartment_number),))

    rows: list[dict[str, Any]] = []
    for row in cur.fetchall():
        item = _row_to_dict(row)
        if not service_scope_match(scope, item.get("service_code")):
            continue

        amount = float(item.get("amount") or 0)
        allocated = float(item.get("allocated_amount") or 0)
        outstanding = max(0.0, amount - allocated)

        if outstanding > 0.01:
            item["outstanding_amount"] = round(outstanding, 2)
            rows.append(item)

    return rows


def default_policy_message(
    apartment_number: Any,
    service_code: str,
    decision: str,
    debt_total: float,
) -> str:
    apt = text(apartment_number) or "-"
    if decision == "BLOCK":
        return (
            f"По квартире {apt} есть задолженность {money(debt_total)} грн. "
            f"Услуга {service_code} временно недоступна до оплаты или сверки."
        )
    if decision == "WARN":
        return (
            f"По квартире {apt} есть задолженность {money(debt_total)} грн. "
            "Требуется ручное решение оператора."
        )
    return ""


def check_service_allowed(
    conn: sqlite3.Connection,
    apartment_number: Any,
    service_code: str,
) -> dict[str, Any]:
    """
    Main read-only policy check.
    """
    svc = load_service_policy(conn, service_code)

    if not svc:
        return {
            "allowed": False,
            "decision": "ERROR",
            "apartment_number": text(apartment_number),
            "service_code": text(service_code),
            "service_name": "",
            "policy": {},
            "debt": {
                "total": 0.0,
                "services": [],
                "rows": [],
            },
            "message": f"service_code не найден в service_catalog: {service_code}",
        }

    enabled = int(svc.get("access_policy_enabled") or 0)
    scope = text(svc.get("access_policy_scope") or "NONE").upper()
    mode = text(svc.get("access_policy_mode") or "NONE").upper()
    review = int(svc.get("manual_review_required") or 0)
    service_name = text(svc.get("service_name"))
    policy_message = text(svc.get("access_policy_message"))

    policy = {
        "enabled": enabled,
        "scope": scope,
        "mode": mode or "NONE",
        "manual_review_required": review,
    }

    if not enabled or mode in ("", "NONE") or scope in ("", "NONE"):
        return {
            "allowed": True,
            "decision": "ALLOW",
            "apartment_number": text(apartment_number),
            "service_code": text(service_code),
            "service_name": service_name,
            "policy": policy,
            "debt": {
                "total": 0.0,
                "services": [],
                "rows": [],
            },
            "message": "Политика доступа для услуги отключена.",
        }

    rows = find_blocking_debt_rows(conn, apartment_number, scope)
    total = round(sum(float(r.get("outstanding_amount") or 0) for r in rows), 2)
    debt_services = sorted({text(r.get("service_code")) for r in rows if text(r.get("service_code"))})

    if total <= 0.01:
        return {
            "allowed": True,
            "decision": "ALLOW",
            "apartment_number": text(apartment_number),
            "service_code": text(service_code),
            "service_name": service_name,
            "policy": policy,
            "debt": {
                "total": 0.0,
                "services": [],
                "rows": [],
            },
            "message": "Блокирующей задолженности не найдено.",
        }

    if mode == "BLOCK":
        return {
            "allowed": False,
            "decision": "BLOCK",
            "apartment_number": text(apartment_number),
            "service_code": text(service_code),
            "service_name": service_name,
            "policy": policy,
            "debt": {
                "total": total,
                "services": debt_services,
                "rows": rows,
            },
            "message": policy_message or default_policy_message(apartment_number, service_code, "BLOCK", total),
        }

    if mode == "WARN":
        return {
            "allowed": True,
            "decision": "WARN",
            "apartment_number": text(apartment_number),
            "service_code": text(service_code),
            "service_name": service_name,
            "policy": policy,
            "debt": {
                "total": total,
                "services": debt_services,
                "rows": rows,
            },
            "message": policy_message or default_policy_message(apartment_number, service_code, "WARN", total),
        }

    return {
        "allowed": True,
        "decision": "ALLOW",
        "apartment_number": text(apartment_number),
        "service_code": text(service_code),
        "service_name": service_name,
        "policy": policy,
        "debt": {
            "total": total,
            "services": debt_services,
            "rows": rows,
        },
        "message": f"Неизвестный режим политики {mode}; в v1 трактуем как ALLOW.",
    }


def result_to_short_text(result: dict[str, Any]) -> str:
    """
    Helper for Telegram/UI messages.
    """
    service = result.get("service_name") or result.get("service_code") or "-"
    decision = result.get("decision")
    debt = result.get("debt") or {}
    total = float(debt.get("total") or 0)
    message = result.get("message") or ""

    if decision == "ALLOW":
        return f"✅ Услуга доступна: {service}"

    if decision == "WARN":
        return f"⚠️ {message}\n\nУслуга: {service}\nЗадолженность: {money(total)} грн."

    if decision == "BLOCK":
        return f"⛔ {message}\n\nУслуга: {service}\nЗадолженность: {money(total)} грн."

    return f"⚠️ Проверка услуги завершилась ошибкой: {message}"
