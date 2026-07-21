# -*- coding: utf-8 -*-
"""
OSBB phone access to two barriers — additive schema and policy core.

This module is intentionally schema/business-rule only. It does NOT:
- send commands to real barriers;
- modify existing service orders, payments, phone credentials or remotes;
- create recurring charges automatically;
- deactivate any existing phone access.

It creates the additive tables needed for a later sandbox implementation:
- access points;
- effective-dated tariffs and policies;
- phone-access subscriptions;
- per-barrier access grants;
- subscription charges;
- debt warnings;
- external controller-command journal;
- immutable operating journal.

All prices and debt-deactivation terms are data, never hard-coded in workflows.
"""

from __future__ import annotations

import calendar
import json
import sqlite3
from datetime import date, datetime
from typing import Any, Iterable


SCHEMA_MIGRATION_CODE = "PHONE_BARRIER_ACCESS_SCHEMA_V1"

ACCESS_POLICY_SET = "PHONE_BARRIER_ACCESS"

BARRIER_FAR_01 = "BARRIER_FAR_01"
BARRIER_NEAR_02 = "BARRIER_NEAR_02"
GENERIC_ACCESS_POINT_SCOPE = "*"

TARIFF_CONNECT = "PHONE_BARRIER_ACCESS_CONNECT"
TARIFF_MONTHLY = "PHONE_BARRIER_ACCESS_MONTHLY"

POLICY_DEBT_GRACE_DAYS = "PHONE_ACCESS_DEBT_GRACE_DAYS"
POLICY_MONTHLY_START_RULE = "PHONE_ACCESS_MONTHLY_START_RULE"
POLICY_AUTO_DEACTIVATE_ENABLED = "PHONE_ACCESS_AUTO_DEACTIVATE_ENABLED"
POLICY_DEFAULT_PARKING_DEBT_MODE = "PHONE_ACCESS_DEFAULT_PARKING_DEBT_MODE"
POLICY_REAPPLICATION_NEW_SUBSCRIPTION = "PHONE_ACCESS_REAPPLICATION_NEW_SUBSCRIPTION"

MONTHLY_START_RULE = "MIDPOINT_OF_CALENDAR_MONTH"


def now_db() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_db() -> str:
    return date.today().isoformat()


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def quote(identifier: str) -> str:
    return '"' + str(identifier).replace('"', '""') + '"'


def table_exists(cur: sqlite3.Cursor, table: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?",
        (table,),
    )
    return cur.fetchone() is not None


def table_columns(cur: sqlite3.Cursor, table: str) -> set[str]:
    if not table_exists(cur, table):
        return set()
    cur.execute(f"PRAGMA table_info({quote(table)})")
    return {str(row[1]) for row in cur.fetchall()}


def as_dict(row: sqlite3.Row | tuple | None, columns: Iterable[str] = ()) -> dict | None:
    if row is None:
        return None
    if isinstance(row, sqlite3.Row):
        return dict(row)
    names = list(columns)
    if not names:
        raise TypeError("A tuple row needs explicit column names.")
    return dict(zip(names, row))


def parse_iso_date(value: str | date | datetime | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(text(value))


def first_charge_period(activation_date: str | date | datetime) -> str:
    """
    Return YYYY-MM according to the approved midpoint rule.

    A registration on or before half of the calendar month is charged for
    the current month. A registration after that half starts next month.

    Exact rule:
        day * 2 <= number_of_days_in_month -> current month
        day * 2 >  number_of_days_in_month -> next month
    """
    activated = parse_iso_date(activation_date)
    days_in_month = calendar.monthrange(activated.year, activated.month)[1]
    if activated.day * 2 <= days_in_month:
        return f"{activated.year:04d}-{activated.month:02d}"
    if activated.month == 12:
        return f"{activated.year + 1:04d}-01"
    return f"{activated.year:04d}-{activated.month + 1:02d}"


def required_phone_access_tables() -> set[str]:
    return {
        "access_schema_migrations",
        "access_points",
        "access_tariff_versions",
        "access_policy_versions",
        "access_policy_values",
        "phone_access_subscriptions",
        "phone_access_subscription_points",
        "phone_access_subscription_charges",
        "access_debt_warnings",
        "access_external_commands",
        "access_operation_journal",
    }


def _fetchone_dict(
    cur: sqlite3.Cursor,
    sql: str,
    params: tuple[Any, ...] = (),
) -> dict | None:
    cur.execute(sql, params)
    row = cur.fetchone()
    if row is None:
        return None
    if isinstance(row, sqlite3.Row):
        return dict(row)
    cols = [str(item[0]) for item in cur.description or []]
    return dict(zip(cols, row))


def _created_tables(cur: sqlite3.Cursor) -> set[str]:
    return {
        str(row[0])
        for row in cur.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }


def _create_schema(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_schema_migrations (
            migration_code TEXT PRIMARY KEY,
            schema_version TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            applied_by TEXT,
            sandbox_db_path TEXT,
            note TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_points (
            id INTEGER PRIMARY KEY,
            access_point_code TEXT NOT NULL UNIQUE,
            display_name_uk TEXT NOT NULL,
            display_name_ru TEXT NOT NULL,
            display_name_en TEXT NOT NULL,
            point_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(point_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            controller_type TEXT,
            controller_reference TEXT,
            is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            retired_at TEXT,
            retired_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_points_active
        ON access_points(is_active, point_status, access_point_code)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_tariff_versions (
            id INTEGER PRIMARY KEY,
            tariff_code TEXT NOT NULL,
            tariff_name_uk TEXT NOT NULL,
            tariff_name_ru TEXT NOT NULL,
            tariff_name_en TEXT NOT NULL,
            access_point_scope_code TEXT NOT NULL DEFAULT '*',
            charge_kind TEXT NOT NULL
                CHECK(charge_kind IN ('CONNECT', 'MONTHLY')),
            billing_period TEXT NOT NULL
                CHECK(billing_period IN ('ONE_TIME', 'MONTHLY')),
            unit_of_measure TEXT NOT NULL DEFAULT 'PER_ACCESS_POINT',
            amount REAL NOT NULL CHECK(amount >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            version_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(version_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            approved_by TEXT,
            approval_reference TEXT,
            change_reason TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(tariff_code, access_point_scope_code, effective_from)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_tariff_lookup
        ON access_tariff_versions(
            tariff_code, access_point_scope_code, version_status, effective_from, effective_to
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_policy_versions (
            id INTEGER PRIMARY KEY,
            policy_set_code TEXT NOT NULL,
            version_number INTEGER NOT NULL CHECK(version_number > 0),
            policy_status TEXT NOT NULL DEFAULT 'ACTIVE'
                CHECK(policy_status IN ('DRAFT', 'ACTIVE', 'RETIRED', 'ARCHIVED')),
            effective_from TEXT NOT NULL,
            effective_to TEXT,
            approved_by TEXT,
            approval_reference TEXT,
            change_reason TEXT,
            created_by TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_set_code, version_number),
            UNIQUE(policy_set_code, effective_from)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_policy_lookup
        ON access_policy_versions(policy_set_code, policy_status, effective_from, effective_to)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_policy_values (
            id INTEGER PRIMARY KEY,
            policy_version_id INTEGER NOT NULL,
            setting_code TEXT NOT NULL,
            value_type TEXT NOT NULL
                CHECK(value_type IN ('TEXT', 'INTEGER', 'BOOLEAN', 'JSON')),
            value_text TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(policy_version_id, setting_code)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_policy_values_code
        ON access_policy_values(setting_code, policy_version_id)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phone_access_subscriptions (
            id INTEGER PRIMARY KEY,
            subscription_number TEXT NOT NULL UNIQUE,
            resident_account_id INTEGER,
            authorised_person_id INTEGER,
            unit_id INTEGER,
            apartment_id INTEGER,
            apartment_number TEXT,
            holder_type TEXT NOT NULL DEFAULT 'RESIDENT'
                CHECK(holder_type IN ('RESIDENT', 'TENANT', 'AUTHORISED_PERSON')),
            phone_normalized TEXT NOT NULL,
            subscription_status TEXT NOT NULL DEFAULT 'PENDING_ACTIVATION'
                CHECK(subscription_status IN (
                    'PENDING_ACTIVATION', 'ACTIVE', 'PARTIALLY_ACTIVE',
                    'DEBT_WARNING', 'DEACTIVATING', 'DEACTIVATED_FOR_DEBT',
                    'DEACTIVATED_MANUAL', 'CLOSED', 'CANCELLED'
                )),
            parking_debt_check_mode TEXT NOT NULL DEFAULT 'MANUAL_REVIEW'
                CHECK(parking_debt_check_mode IN (
                    'CHECK_LINKED_PARKING_ACCOUNT',
                    'NOT_APPLICABLE_NO_PARKING',
                    'MANUAL_REVIEW'
                )),
            parking_debt_check_note TEXT,
            parking_debt_mode_set_by TEXT,
            parking_debt_mode_set_at TEXT,
            activation_date TEXT,
            first_charge_period TEXT,
            monthly_start_policy_version_id INTEGER,
            connect_tariff_version_id INTEGER,
            monthly_tariff_version_id INTEGER,
            created_from_order_id INTEGER,
            created_from_interest_id INTEGER,
            closed_at TEXT,
            close_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phone_access_subscriptions_status
        ON phone_access_subscriptions(subscription_status, apartment_id, phone_normalized)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phone_access_subscriptions_phone
        ON phone_access_subscriptions(phone_normalized, subscription_status)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phone_access_subscription_points (
            id INTEGER PRIMARY KEY,
            subscription_id INTEGER NOT NULL,
            access_point_code TEXT NOT NULL,
            access_point_name_snapshot TEXT NOT NULL,
            point_status TEXT NOT NULL DEFAULT 'PENDING_ACTIVATION'
                CHECK(point_status IN (
                    'PENDING_ACTIVATION', 'ACTIVE', 'SUSPENDED_FOR_DEBT',
                    'DEACTIVATED_FOR_DEBT', 'DEACTIVATED_MANUAL',
                    'EXTERNAL_SYNC_ERROR', 'CANCELLED'
                )),
            activated_at TEXT,
            deactivated_at TEXT,
            deactivation_reason TEXT,
            external_controller_reference TEXT,
            last_external_sync_status TEXT,
            last_external_sync_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(subscription_id, access_point_code)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phone_access_points_status
        ON phone_access_subscription_points(subscription_id, point_status, access_point_code)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phone_access_subscription_charges (
            id INTEGER PRIMARY KEY,
            charge_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            subscription_point_id INTEGER,
            access_point_code TEXT NOT NULL,
            charge_kind TEXT NOT NULL
                CHECK(charge_kind IN ('CONNECT', 'MONTHLY')),
            charge_period_key TEXT NOT NULL,
            billing_period TEXT,
            tariff_code TEXT NOT NULL,
            tariff_version_id INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
            unit_price_snapshot REAL NOT NULL CHECK(unit_price_snapshot >= 0),
            amount_due_snapshot REAL NOT NULL CHECK(amount_due_snapshot >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            due_date TEXT,
            charge_status TEXT NOT NULL DEFAULT 'DRAFT'
                CHECK(charge_status IN (
                    'DRAFT', 'OPEN', 'PAID', 'OVERDUE', 'WAIVED', 'CANCELLED'
                )),
            service_order_id INTEGER,
            payment_notice_id INTEGER,
            payment_id INTEGER,
            posted_at TEXT,
            paid_at TEXT,
            cancelled_at TEXT,
            cancellation_reason TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(subscription_point_id, charge_kind, charge_period_key)
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phone_access_charges_due
        ON phone_access_subscription_charges(subscription_id, charge_status, due_date, billing_period)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phone_access_charges_payment
        ON phone_access_subscription_charges(payment_id, payment_notice_id)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_debt_warnings (
            id INTEGER PRIMARY KEY,
            warning_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            debt_source TEXT NOT NULL
                CHECK(debt_source IN (
                    'PARKING_ARREARS',
                    'PHONE_ACCESS_SUBSCRIPTION_ARREARS'
                )),
            source_charge_id INTEGER,
            debt_amount_snapshot REAL NOT NULL CHECK(debt_amount_snapshot >= 0),
            currency TEXT NOT NULL DEFAULT 'UAH',
            source_reference TEXT,
            detected_at TEXT NOT NULL,
            warning_sent_at TEXT,
            grace_days_snapshot INTEGER NOT NULL CHECK(grace_days_snapshot >= 0),
            deactivate_due_at TEXT NOT NULL,
            policy_version_id INTEGER,
            warning_status TEXT NOT NULL DEFAULT 'OPEN'
                CHECK(warning_status IN (
                    'OPEN', 'RESOLVED', 'CANCELLED',
                    'DEACTIVATION_QUEUED', 'DEACTIVATED'
                )),
            resolved_at TEXT,
            resolution_note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_debt_warnings_due
        ON access_debt_warnings(warning_status, deactivate_due_at, subscription_id)
        """
    )
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ux_access_debt_warning_open
        ON access_debt_warnings(subscription_id, debt_source)
        WHERE warning_status IN ('OPEN', 'DEACTIVATION_QUEUED')
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_external_commands (
            id INTEGER PRIMARY KEY,
            command_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER NOT NULL,
            subscription_point_id INTEGER NOT NULL,
            access_point_code TEXT NOT NULL,
            command_action TEXT NOT NULL
                CHECK(command_action IN ('ACTIVATE', 'DEACTIVATE')),
            phone_snapshot TEXT NOT NULL,
            command_status TEXT NOT NULL DEFAULT 'QUEUED'
                CHECK(command_status IN (
                    'QUEUED', 'SENT', 'CONFIRMED', 'FAILED',
                    'RETRY_SCHEDULED', 'CANCELLED'
                )),
            attempt_number INTEGER NOT NULL DEFAULT 0 CHECK(attempt_number >= 0),
            external_correlation_id TEXT,
            payload_json TEXT,
            last_error TEXT,
            queued_at TEXT NOT NULL,
            sent_at TEXT,
            confirmed_at TEXT,
            failed_at TEXT,
            retry_at TEXT,
            created_by TEXT,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_external_commands_queue
        ON access_external_commands(command_status, retry_at, access_point_code, id)
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS access_operation_journal (
            id INTEGER PRIMARY KEY,
            event_number TEXT NOT NULL UNIQUE,
            subscription_id INTEGER,
            subscription_point_id INTEGER,
            access_point_code TEXT,
            event_type TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT,
            actor_id TEXT,
            source_context TEXT,
            correlation_id TEXT,
            payload_json TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_operation_journal_subscription
        ON access_operation_journal(subscription_id, created_at, id)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_access_operation_journal_point
        ON access_operation_journal(subscription_point_id, created_at, id)
        """
    )


def _record_change(
    cur: sqlite3.Cursor,
    *,
    event_number: str,
    event_type: str,
    source_context: str,
    payload: dict[str, Any],
    actor_id: str = "schema_migration",
) -> None:
    cur.execute(
        """
        INSERT OR IGNORE INTO access_operation_journal (
            event_number, event_type, actor_id, source_context, payload_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            event_number,
            event_type,
            actor_id,
            source_context,
            json.dumps(payload, ensure_ascii=False, sort_keys=True),
            now_db(),
        ),
    )


def _ensure_access_point(
    cur: sqlite3.Cursor,
    *,
    code: str,
    uk: str,
    ru: str,
    en: str,
    effective_from: str,
) -> bool:
    existing = _fetchone_dict(
        cur,
        "SELECT * FROM access_points WHERE access_point_code = ?",
        (code,),
    )
    if existing:
        return False
    cur.execute(
        """
        INSERT INTO access_points (
            access_point_code, display_name_uk, display_name_ru, display_name_en,
            point_status, is_active, effective_from, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, 'ACTIVE', 1, ?, ?, ?)
        """,
        (code, uk, ru, en, effective_from, now_db(), now_db()),
    )
    return True


def _ensure_tariff(
    cur: sqlite3.Cursor,
    *,
    tariff_code: str,
    uk: str,
    ru: str,
    en: str,
    charge_kind: str,
    billing_period: str,
    amount: float,
    effective_from: str,
    created_by: str,
) -> bool:
    existing = _fetchone_dict(
        cur,
        """
        SELECT *
        FROM access_tariff_versions
        WHERE tariff_code = ?
          AND access_point_scope_code = ?
          AND effective_from = ?
        """,
        (tariff_code, GENERIC_ACCESS_POINT_SCOPE, effective_from),
    )
    if existing:
        expected = (float(amount), charge_kind, billing_period, "UAH")
        actual = (
            float(existing["amount"]),
            text(existing["charge_kind"]),
            text(existing["billing_period"]),
            text(existing["currency"]),
        )
        if actual != expected:
            raise RuntimeError(
                "Найдена существующая тарифная версия с тем же кодом и датой, "
                f"но другими данными: {tariff_code} / {effective_from}."
            )
        return False

    cur.execute(
        """
        INSERT INTO access_tariff_versions (
            tariff_code, tariff_name_uk, tariff_name_ru, tariff_name_en,
            access_point_scope_code, charge_kind, billing_period, unit_of_measure,
            amount, currency, effective_from, version_status, approval_reference,
            change_reason, created_by, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'PER_ACCESS_POINT',
                ?, 'UAH', ?, 'ACTIVE', ?, ?, ?, ?, ?)
        """,
        (
            tariff_code,
            uk,
            ru,
            en,
            GENERIC_ACCESS_POINT_SCOPE,
            charge_kind,
            billing_period,
            float(amount),
            effective_from,
            "SANDBOX_INITIAL_SEED",
            "Initial agreed phone-barrier tariff for sandbox.",
            created_by,
            now_db(),
            now_db(),
        ),
    )
    return True


def _ensure_policy_version(
    cur: sqlite3.Cursor,
    *,
    effective_from: str,
    created_by: str,
) -> tuple[int, bool]:
    existing = _fetchone_dict(
        cur,
        """
        SELECT *
        FROM access_policy_versions
        WHERE policy_set_code = ? AND effective_from = ?
        """,
        (ACCESS_POLICY_SET, effective_from),
    )
    if existing:
        return int(existing["id"]), False

    cur.execute(
        """
        SELECT COALESCE(MAX(version_number), 0) + 1
        FROM access_policy_versions
        WHERE policy_set_code = ?
        """,
        (ACCESS_POLICY_SET,),
    )
    version_number = int(cur.fetchone()[0])
    cur.execute(
        """
        INSERT INTO access_policy_versions (
            policy_set_code, version_number, policy_status, effective_from,
            approval_reference, change_reason, created_by, created_at, updated_at
        )
        VALUES (?, ?, 'ACTIVE', ?, ?, ?, ?, ?, ?)
        """,
        (
            ACCESS_POLICY_SET,
            version_number,
            effective_from,
            "SANDBOX_INITIAL_SEED",
            "Initial agreed phone-barrier policy for sandbox.",
            created_by,
            now_db(),
            now_db(),
        ),
    )
    return int(cur.lastrowid), True


def _ensure_policy_value(
    cur: sqlite3.Cursor,
    *,
    policy_version_id: int,
    setting_code: str,
    value_type: str,
    value_text: str,
    description: str,
) -> bool:
    existing = _fetchone_dict(
        cur,
        """
        SELECT *
        FROM access_policy_values
        WHERE policy_version_id = ? AND setting_code = ?
        """,
        (int(policy_version_id), setting_code),
    )
    if existing:
        expected = (value_type, value_text)
        actual = (text(existing["value_type"]), text(existing["value_text"]))
        if actual != expected:
            raise RuntimeError(
                "Найдена существующая настройка политики с другим значением: "
                f"{setting_code}."
            )
        return False
    cur.execute(
        """
        INSERT INTO access_policy_values (
            policy_version_id, setting_code, value_type, value_text,
            description, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            int(policy_version_id),
            setting_code,
            value_type,
            value_text,
            description,
            now_db(),
            now_db(),
        ),
    )
    return True


def active_policy_values(
    *,
    as_of: str | date | datetime | None = None,
    conn: sqlite3.Connection,
) -> dict[str, str]:
    """Return the active phone-barrier policy values for a given date."""
    when = parse_iso_date(as_of).isoformat()
    cur = conn.cursor()
    row = _fetchone_dict(
        cur,
        """
        SELECT *
        FROM access_policy_versions
        WHERE policy_set_code = ?
          AND policy_status = 'ACTIVE'
          AND effective_from <= ?
          AND (effective_to IS NULL OR effective_to >= ?)
        ORDER BY effective_from DESC, version_number DESC
        LIMIT 1
        """,
        (ACCESS_POLICY_SET, when, when),
    )
    if not row:
        raise LookupError("Не найдена активная политика телефонного доступа.")
    cur.execute(
        """
        SELECT setting_code, value_text
        FROM access_policy_values
        WHERE policy_version_id = ?
        ORDER BY setting_code
        """,
        (int(row["id"]),),
    )
    return {text(item[0]): text(item[1]) for item in cur.fetchall()}


def resolve_tariff(
    *,
    tariff_code: str,
    access_point_code: str,
    as_of: str | date | datetime | None = None,
    conn: sqlite3.Connection,
) -> dict:
    """
    Return a current tariff snapshot.

    A tariff specifically assigned to the selected access point wins over
    the generic '*' tariff. This supports future price differences without
    redesigning the schema.
    """
    when = parse_iso_date(as_of).isoformat()
    cur = conn.cursor()
    row = _fetchone_dict(
        cur,
        """
        SELECT *
        FROM access_tariff_versions
        WHERE tariff_code = ?
          AND access_point_scope_code IN (?, ?)
          AND version_status = 'ACTIVE'
          AND effective_from <= ?
          AND (effective_to IS NULL OR effective_to >= ?)
        ORDER BY
          CASE WHEN access_point_scope_code = ? THEN 0 ELSE 1 END,
          effective_from DESC,
          id DESC
        LIMIT 1
        """,
        (
            tariff_code,
            access_point_code,
            GENERIC_ACCESS_POINT_SCOPE,
            when,
            when,
            access_point_code,
        ),
    )
    if not row:
        raise LookupError(
            f"Не найден активный тариф {tariff_code} для {access_point_code}."
        )
    return row


def ensure_phone_barrier_access_schema(
    conn: sqlite3.Connection,
    *,
    effective_from: str | date | datetime | None = None,
    actor_id: str = "schema_migration",
    sandbox_db_path: str = "",
) -> list[str]:
    """
    Create additive tables and seed only the agreed initial sandbox values.

    The caller owns the transaction. No commit/rollback is performed here.
    """
    effective = parse_iso_date(effective_from).isoformat()
    cur = conn.cursor()
    before = _created_tables(cur)
    _create_schema(cur)
    after = _created_tables(cur)

    changes: list[str] = []
    created = sorted(required_phone_access_tables() - before)
    for table in created:
        changes.append(f"created table {table}")

    if _ensure_access_point(
        cur,
        code=BARRIER_FAR_01,
        uk="Далекий шлагбаум №1",
        ru="Дальний шлагбаум №1",
        en="Far barrier No. 1",
        effective_from=effective,
    ):
        changes.append(f"seeded access point {BARRIER_FAR_01}")

    if _ensure_access_point(
        cur,
        code=BARRIER_NEAR_02,
        uk="Ближній шлагбаум №2",
        ru="Ближний шлагбаум №2",
        en="Near barrier No. 2",
        effective_from=effective,
    ):
        changes.append(f"seeded access point {BARRIER_NEAR_02}")

    if _ensure_tariff(
        cur,
        tariff_code=TARIFF_CONNECT,
        uk="Підключення телефону до одного шлагбаума",
        ru="Подключение телефона к одному шлагбауму",
        en="Phone connection to one barrier",
        charge_kind="CONNECT",
        billing_period="ONE_TIME",
        amount=200.0,
        effective_from=effective,
        created_by=actor_id,
    ):
        changes.append("seeded tariff PHONE_BARRIER_ACCESS_CONNECT = 200 UAH per barrier")

    if _ensure_tariff(
        cur,
        tariff_code=TARIFF_MONTHLY,
        uk="Абонплата за телефонний доступ до одного шлагбаума",
        ru="Абонплата за телефонный доступ к одному шлагбауму",
        en="Monthly phone access for one barrier",
        charge_kind="MONTHLY",
        billing_period="MONTHLY",
        amount=100.0,
        effective_from=effective,
        created_by=actor_id,
    ):
        changes.append("seeded tariff PHONE_BARRIER_ACCESS_MONTHLY = 100 UAH per barrier/month")

    policy_id, policy_created = _ensure_policy_version(
        cur,
        effective_from=effective,
        created_by=actor_id,
    )
    if policy_created:
        changes.append(
            f"seeded policy {ACCESS_POLICY_SET} version for {effective}"
        )

    policy_values = [
        (
            POLICY_DEBT_GRACE_DAYS,
            "INTEGER",
            "10",
            "Grace period after a confirmed debt warning, in calendar days.",
        ),
        (
            POLICY_MONTHLY_START_RULE,
            "TEXT",
            MONTHLY_START_RULE,
            "Current month up to the month midpoint; next month after it.",
        ),
        (
            POLICY_AUTO_DEACTIVATE_ENABLED,
            "BOOLEAN",
            "1",
            "After the grace deadline, deactivate all selected access points.",
        ),
        (
            POLICY_DEFAULT_PARKING_DEBT_MODE,
            "TEXT",
            "MANUAL_REVIEW",
            "Safe default: no automatic parking-debt action until verified.",
        ),
        (
            POLICY_REAPPLICATION_NEW_SUBSCRIPTION,
            "BOOLEAN",
            "1",
            "Re-access after debt deactivation creates a new subscription.",
        ),
    ]
    for code, value_type, value, description in policy_values:
        if _ensure_policy_value(
            cur,
            policy_version_id=policy_id,
            setting_code=code,
            value_type=value_type,
            value_text=value,
            description=description,
        ):
            changes.append(f"seeded policy value {code} = {value}")

    prior = _fetchone_dict(
        cur,
        "SELECT migration_code FROM access_schema_migrations WHERE migration_code = ?",
        (SCHEMA_MIGRATION_CODE,),
    )
    if not prior:
        cur.execute(
            """
            INSERT INTO access_schema_migrations (
                migration_code, schema_version, applied_at, applied_by,
                sandbox_db_path, note
            )
            VALUES (?, '1.0', ?, ?, ?, ?)
            """,
            (
                SCHEMA_MIGRATION_CODE,
                now_db(),
                actor_id,
                sandbox_db_path,
                "Additive sandbox schema for two-barrier phone access.",
            ),
        )
        changes.append(f"recorded migration {SCHEMA_MIGRATION_CODE}")
        _record_change(
            cur,
            event_number=f"MIG-{SCHEMA_MIGRATION_CODE}",
            event_type="SCHEMA_MIGRATION_APPLIED",
            source_context="phone_barrier_access_schema",
            payload={
                "migration_code": SCHEMA_MIGRATION_CODE,
                "effective_from": effective,
                "created_tables": created,
            },
            actor_id=actor_id,
        )

    return changes or ["schema and initial sandbox policy already present"]
