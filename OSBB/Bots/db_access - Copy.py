from pathlib import Path
import sys
import sqlite3
from datetime import datetime


BOT_DIR = Path(__file__).resolve().parent
OSBB_ROOT = BOT_DIR.parent
PY_ROOT = OSBB_ROOT.parent

for p in (OSBB_ROOT, PY_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# from config import paths
from config import paths, USE_TEST_DB

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# USE_TEST_DB = True
# USE_TEST_DB = False

def get_conn():
    if USE_TEST_DB:
        return sqlite3.connect(paths.OSBB_TEST_DB_FILE)
    return sqlite3.connect(paths.OSBB_DB_FILE)


# ==========================================================
# Admin / permissions
# ==========================================================

def get_admin_record(telegram_user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            telegram_user_id,
            telegram_username,
            display_name,
            role,
            can_read,
            can_write,
            can_manage_users,
            can_manage_payments,
            can_manage_bot,
            is_active
        FROM bot_admins
        WHERE telegram_user_id = ?
          AND is_active = 1
    """, (int(telegram_user_id),))

    row = cur.fetchone()
    conn.close()

    return row


def is_admin(telegram_user_id):
    return get_admin_record(telegram_user_id) is not None


def is_super_admin(telegram_user_id):
    row = get_admin_record(telegram_user_id)

    if not row:
        return False

    return row[3] == "super_admin"


def can_write(telegram_user_id):
    row = get_admin_record(telegram_user_id)

    if not row:
        return False

    return bool(row[5])


def can_manage_users(telegram_user_id):
    row = get_admin_record(telegram_user_id)

    if not row:
        return False

    return bool(row[6])


# ==========================================================
# Resident accounts
# ==========================================================

def upsert_resident_account_from_telegram(user, language_code="ru"):
    """
    Создаёт/обновляет resident_accounts по Telegram user.
    Квартиру не привязывает.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resident_accounts (
            telegram_user_id,
            telegram_username,
            telegram_first_name,
            telegram_last_name,
            role,
            status,
            language_code,
            created_at,
            updated_at,
            last_seen_at
        )
        VALUES (?, ?, ?, ?, 'resident', 'new', ?, ?, ?, ?)

        ON CONFLICT(telegram_user_id)
        DO UPDATE SET
            telegram_username = excluded.telegram_username,
            telegram_first_name = excluded.telegram_first_name,
            telegram_last_name = excluded.telegram_last_name,
            language_code = excluded.language_code,
            updated_at = excluded.updated_at,
            last_seen_at = excluded.last_seen_at
    """, (
        int(user.id),
        user.username,
        user.first_name,
        user.last_name,
        language_code,
        now(),
        now(),
        now(),
    ))
    #    

    conn.commit()
    conn.close()


def get_resident_account(telegram_user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            telegram_user_id,
            telegram_username,
            telegram_first_name,
            telegram_last_name,
            apartment_id,
            apartment_number,
            role,
            status,
            language_code,
            created_at,
            updated_at,
            verified_at,
            last_seen_at,
            notes
        FROM resident_accounts
        WHERE telegram_user_id = ?
    """, (int(telegram_user_id),))

    row = cur.fetchone()
    conn.close()

    return row


def get_accounts_by_apartment(apartment_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            telegram_user_id,
            telegram_username,
            telegram_first_name,
            telegram_last_name,
            role,
            status,
            verified_at
        FROM resident_accounts
        WHERE apartment_number = ?
        ORDER BY verified_at, telegram_user_id
    """, (str(apartment_number),))

    rows = cur.fetchall()
    conn.close()

    return rows

# 
# 
def get_resident_accounts_summary(limit=10):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM resident_accounts
    """)
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM resident_accounts
        WHERE apartment_number IS NOT NULL
          AND TRIM(apartment_number) <> ''
    """)
    linked = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM resident_accounts
        WHERE apartment_number IS NULL
           OR TRIM(apartment_number) = ''
    """)
    unlinked = cur.fetchone()[0]

    cur.execute("""
        SELECT
            telegram_user_id,
            telegram_username,
            telegram_first_name,
            telegram_last_name,
            apartment_number,
            status,
            last_seen_at
        FROM resident_accounts
        ORDER BY
            COALESCE(last_seen_at, updated_at, created_at) DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return {
        "total": total,
        "linked": linked,
        "unlinked": unlinked,
        "rows": rows,
    }


def format_resident_accounts_summary(summary):
    lines = []

    lines.append("👥 Пользователи")
    lines.append("")
    lines.append(f"Всего: {summary['total']}")
    lines.append(f"С квартирой: {summary['linked']}")
    lines.append(f"Без квартиры: {summary['unlinked']}")
    lines.append("")
    lines.append("Последние:")

    if not summary["rows"]:
        lines.append("пока нет пользователей")
        return "\n".join(lines)

    for row in summary["rows"]:
        (
            telegram_user_id,
            username,
            first_name,
            last_name,
            apartment_number,
            status,
            last_seen_at,
        ) = row

        name_parts = [
            x for x in [first_name, last_name]
            if x
        ]

        display_name = " ".join(name_parts) or "-"
        username_text = f"@{username}" if username else "-"
        apt = apartment_number or "-"
        status = status or "-"

        lines.append(
            f"• кв.{apt} | {display_name} | "
            f"{username_text} | {status}"
        )

    return "\n".join(lines)


def find_apartment(apartment_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            apartment_number,
            entrance
        FROM apartments
        WHERE apartment_number = ?
    """, (str(apartment_number),))

    row = cur.fetchone()
    conn.close()

    return row


def link_resident_to_apartment(telegram_user_id, apartment_number, status="apartment_confirmed"):
    apt = find_apartment(apartment_number)

    if not apt:
        return False, "apartment_not_found"

    apartment_id = apt[0]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE resident_accounts
        SET
            apartment_id = ?,
            apartment_number = ?,
            status = ?,
            verified_at = ?,
            updated_at = ?
        WHERE telegram_user_id = ?
    """, (
        apartment_id,
        str(apartment_number),
        status,
        now(),
        now(),
        int(telegram_user_id),
    ))

    conn.commit()
    conn.close()

    return True, "linked"


# ==========================================================
# Apartments / vehicles
# ==========================================================

def get_apartment_vehicles(apartment_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM apartments
        WHERE apartment_number = ?
    """, (str(apartment_number),))

    apt = cur.fetchone()

    if not apt:
        conn.close()
        return []

    apartment_id = apt[0]

    cur.execute("""
        SELECT
            id,
            license_plate_normalized,
            license_plate,
            car_model_normalized,
            car_model,
            parking_time
        FROM vehicles
        WHERE apartment_id = ?
        ORDER BY id
    """, (apartment_id,))

    rows = cur.fetchall()
    conn.close()

    return rows


def format_vehicle_list(vehicles):
    if not vehicles:
        return "Автомобили пока не найдены."

    lines = []

    for (
        vehicle_id,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) in vehicles:
        plate = plate_norm or plate_raw or "-"
        model = model_norm or model_raw or "-"
        pt = parking_time or "не указан"

        lines.append(
            f"• {plate} | {model} | тариф: {pt}"
        )

    return "\n".join(lines)


# ==========================================================
# Audit log
# ==========================================================

def write_audit_log(
    telegram_user_id,
    action_type,
    table_name=None,
    record_id=None,
    old_value=None,
    new_value=None,
    actor_role=None,
    actor_name=None,
    comment=None,
    source="bot",
):
    conn = get_conn()
    cur = conn.cursor()

    # В вашей БД audit_log уже имеет старую структуру:
    # event_time, username, action, field_name, comment...
    cur.execute("""
        INSERT INTO audit_log (
            event_time,
            telegram_user_id,
            username,
            actor_role,
            actor_name,
            action,
            action_type,
            table_name,
            record_id,
            old_value,
            new_value,
            comment,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now(),
        int(telegram_user_id) if telegram_user_id else None,
        str(telegram_user_id) if telegram_user_id else None,
        actor_role,
        actor_name,
        action_type,
        action_type,
        table_name,
        str(record_id) if record_id is not None else None,
        old_value,
        new_value,
        comment,
        source,
    ))

    conn.commit()
    conn.close()
#  -----------
# append 
# ==========================================================
# Resident accounts - admin lists and operator verification
# Add this block into Bots\db_access.py after resident account functions.
# ==========================================================

def get_resident_accounts_by_filter(filter_name="all", limit=30):
    conn = get_conn()
    cur = conn.cursor()

    where = ""

    if filter_name == "without_apartment":
        where = """
        WHERE apartment_number IS NULL
           OR TRIM(apartment_number) = ''
        """
    elif filter_name == "self_confirmed":
        where = """
        WHERE status = 'apartment_confirmed'
        """
    elif filter_name == "operator_verified":
        where = """
        WHERE status = 'operator_verified'
        """

    cur.execute(f"""
        SELECT
            telegram_user_id,
            telegram_username,
            telegram_first_name,
            telegram_last_name,
            apartment_number,
            status,
            last_seen_at
        FROM resident_accounts
        {where}
        ORDER BY
            COALESCE(last_seen_at, updated_at, created_at) DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows


def format_resident_accounts_list(title, rows):
    lines = [f"👥 {title}", ""]

    if not rows:
        lines.append("Список пуст.")
        return "\n".join(lines)

    for row in rows:
        (
            telegram_user_id,
            username,
            first_name,
            last_name,
            apartment_number,
            status,
            last_seen_at,
        ) = row

        name = " ".join(x for x in [first_name, last_name] if x) or "-"
        username_text = f"@{username}" if username else "-"
        apt = apartment_number or "-"
        status = status or "-"

        lines.append(
            f"• ID:{telegram_user_id} | кв.{apt} | "
            f"{name} | {username_text} | {status}"
        )

    return "\n".join(lines)


def get_resident_account_by_telegram_id(telegram_user_id):
    return get_resident_account(int(telegram_user_id))


def format_resident_account_card(account):
    if not account:
        return "Пользователь не найден."

    (
        account_id,
        telegram_user_id,
        telegram_username,
        telegram_first_name,
        telegram_last_name,
        apartment_id,
        apartment_number,
        role,
        status,
        language_code,
        created_at,
        updated_at,
        verified_at,
        last_seen_at,
        notes,
    ) = account

    name = " ".join(
        x for x in [telegram_first_name, telegram_last_name]
        if x
    ) or "-"

    username = f"@{telegram_username}" if telegram_username else "-"

    vehicles = []
    if apartment_number:
        vehicles = get_apartment_vehicles(apartment_number)

    lines = []
    lines.append("👤 Карточка пользователя")
    lines.append("")
    lines.append(f"Telegram ID : {telegram_user_id}")
    lines.append(f"Имя         : {name}")
    lines.append(f"Username    : {username}")
    lines.append(f"Квартира    : {apartment_number or '-'}")
    lines.append(f"Роль        : {role or '-'}")
    lines.append(f"Статус      : {status or '-'}")
    lines.append(f"Язык        : {language_code or '-'}")
    lines.append("")
    lines.append("Автомобили:")
    lines.append(format_vehicle_list(vehicles))

    return "\n".join(lines)


def mark_resident_operator_verified(telegram_user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE resident_accounts
        SET
            status = 'operator_verified',
            updated_at = ?,
            notes = COALESCE(notes, '') || ' | operator_verified'
        WHERE telegram_user_id = ?
    """, (
        now(),
        int(telegram_user_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if changed:
        return True, "operator_verified"

    return False, "user_not_found"


def unlink_resident_account(telegram_user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE resident_accounts
        SET
            apartment_id = NULL,
            apartment_number = NULL,
            status = 'new',
            updated_at = ?,
            notes = COALESCE(notes, '') || ' | apartment_unlinked'
        WHERE telegram_user_id = ?
    """, (
        now(),
        int(telegram_user_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if changed:
        return True, "unlinked"

    return False, "user_not_found"


# ==========================================================
# Vehicle edit workflow
# ==========================================================

def get_vehicle_by_id_for_apartment(vehicle_id, apartment_number=None):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return None

    if apartment_number is not None and str(vehicle[1]) != str(apartment_number):
        return None

    return vehicle


def format_vehicle_card_for_edit(vehicle):
    if not vehicle:
        return "Автомобиль не найден."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = vehicle

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        "🚗 Автомобиль\n\n"
        f"Квартира: {apartment_number}\n"
        f"Номер: {plate}\n"
        f"Марка: {model}\n"
        f"Статус: {status}"
    )


def update_vehicle_parking_status(vehicle_id, status):
    if status == "NULL":
        new_value = None
    elif status in ["Day", "Night", "Inactive"]:
        new_value = status
    else:
        return False, "invalid_status"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_value = vehicle[6]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET parking_time = ?
        WHERE id = ?
    """, (
        new_value,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_value,
        "new_value": new_value,
    }


def update_vehicle_plate(vehicle_id, plate):
    plate = str(plate).strip().upper()

    if not plate:
        return False, "empty_plate"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_plate = vehicle[2]
    old_plate_norm = vehicle[3]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET
            license_plate = ?,
            license_plate_normalized = ?
        WHERE id = ?
    """, (
        plate,
        plate,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_plate_norm or old_plate,
        "new_value": plate,
    }


def update_vehicle_model(vehicle_id, model):
    model = str(model).strip().upper()

    if not model:
        return False, "empty_model"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_model = vehicle[4]
    old_model_norm = vehicle[5]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET
            car_model = ?,
            car_model_normalized = ?
        WHERE id = ?
    """, (
        model,
        model,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_model_norm or old_model,
        "new_value": model,
    }


# ==========================================================
# Compatibility: vehicle review functions
# ==========================================================

def get_next_vehicle_for_review():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id,
            a.apartment_number,
            v.license_plate_normalized,
            v.license_plate,
            v.car_model_normalized,
            v.car_model,
            v.parking_time
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        WHERE
            v.parking_time IS NULL
            OR TRIM(v.parking_time) = ''
        ORDER BY
            CASE
                WHEN a.apartment_number GLOB '[0-9]*'
                THEN CAST(a.apartment_number AS INTEGER)
                ELSE 999999
            END,
            a.apartment_number,
            v.id
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()
    return row


def set_vehicle_day(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Day")


def set_vehicle_night(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Night")


def set_vehicle_inactive(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Inactive")


def skip_vehicle_review(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    return True, {
        "vehicle_id": int(vehicle_id),
        "action": "skipped",
    }


def get_vehicle_review_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vehicles")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Day'")
    day_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Night'")
    night_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Inactive'")
    inactive_count = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM vehicles
        WHERE parking_time IS NULL
           OR TRIM(parking_time) = ''
    """)
    missing_count = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "Day": day_count,
        "Night": night_count,
        "Inactive": inactive_count,
        "missing": missing_count,
    }


def format_vehicle_review_card(vehicle):
    if not vehicle:
        return "Все автомобили уже имеют статус Day / Night / Inactive."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = vehicle

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        "🚗 Проверка автомобиля\n\n"
        f"ID: {vehicle_id}\n"
        f"Квартира: {apartment_number}\n\n"
        f"Номер: {plate}\n"
        f"Марка: {model}\n"
        f"Статус: {status}\n\n"
        "Выберите действие:"
    )


# ==========================================================
# Compatibility: vehicle status lists
# ==========================================================

def get_vehicles_by_status(status_filter="all", limit=50):
    conn = get_conn()
    cur = conn.cursor()

    where = ""

    if status_filter == "missing":
        where = """
        WHERE v.parking_time IS NULL
           OR TRIM(v.parking_time) = ''
        """
    elif status_filter in ["Day", "Night", "Inactive"]:
        where = "WHERE v.parking_time = ?"

    params = []

    if status_filter in ["Day", "Night", "Inactive"]:
        params.append(status_filter)

    params.append(limit)

    cur.execute(f"""
        SELECT
            v.id,
            a.apartment_number,
            v.license_plate_normalized,
            v.license_plate,
            v.car_model_normalized,
            v.car_model,
            v.parking_time
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        {where}
        ORDER BY
            CASE
                WHEN a.apartment_number GLOB '[0-9]*'
                THEN CAST(a.apartment_number AS INTEGER)
                ELSE 999999
            END,
            a.apartment_number,
            v.id
        LIMIT ?
    """, tuple(params))

    rows = cur.fetchall()
    conn.close()
    return rows


def format_vehicle_admin_line(row):
    if not row:
        return "Автомобиль не найден."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = row

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        f"кв.{apartment_number} | "
        f"{plate} | {model} | {status}"
    )


def format_vehicles_admin_list(title, rows):
    count = len(rows)

    lines = [f"🚗 {title}: {count}", ""]

    if not rows:
        lines.append("Список пуст.")
        return "\n".join(lines)

    for row in rows:
        lines.append("• " + format_vehicle_admin_line(row))

    return "\n".join(lines)


# ==========================================================
# REPAIR BLOCK: apartments and vehicle edit compatibility
# ==========================================================

def get_vehicle_by_id(vehicle_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id,
            a.apartment_number,
            v.license_plate_normalized,
            v.license_plate,
            v.car_model_normalized,
            v.car_model,
            v.parking_time
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        WHERE v.id = ?
    """, (int(vehicle_id),))

    row = cur.fetchone()
    conn.close()
    return row


def get_apartment_card(apartment_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            apartment_number,
            entrance
        FROM apartments
        WHERE apartment_number = ?
    """, (str(apartment_number),))

    apartment = cur.fetchone()

    if not apartment:
        conn.close()
        return None

    cur.execute("""
        SELECT
            telegram_first_name,
            telegram_last_name,
            telegram_username,
            status
        FROM resident_accounts
        WHERE apartment_number = ?
        ORDER BY telegram_user_id
    """, (str(apartment_number),))

    residents = cur.fetchall()
    conn.close()

    vehicles = get_apartment_vehicles(apartment_number)

    return {
        "apartment_number": apartment[1],
        "entrance": apartment[2],
        "residents": residents,
        "vehicles": vehicles,
    }


def format_apartment_card(card):
    if not card:
        return "Квартира не найдена."

    residents_count = len(card["residents"])
    vehicles_count = len(card["vehicles"])

    lines = []
    lines.append(f"🏠 Квартира {card['apartment_number']}")
    lines.append("")
    lines.append(f"👥 Жильцы: {residents_count}")
    lines.append(f"🚗 Авто: {vehicles_count}")
    lines.append("")
    lines.append("Выберите раздел:")

    return "\n".join(lines)


def get_vehicle_by_id_for_apartment(vehicle_id, apartment_number=None):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return None

    if apartment_number is not None and str(vehicle[1]) != str(apartment_number):
        return None

    return vehicle


def format_vehicle_card_for_edit(vehicle):
    if not vehicle:
        return "Автомобиль не найден."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = vehicle

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        "🚗 Автомобиль\n\n"
        f"Квартира: {apartment_number}\n"
        f"Номер: {plate}\n"
        f"Марка: {model}\n"
        f"Статус: {status}"
    )


def update_vehicle_parking_status(vehicle_id, status):
    if status == "NULL":
        new_value = None
    elif status in ["Day", "Night", "Inactive"]:
        new_value = status
    else:
        return False, "invalid_status"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_value = vehicle[6]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET parking_time = ?
        WHERE id = ?
    """, (
        new_value,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_value,
        "new_value": new_value,
    }


def update_vehicle_plate(vehicle_id, plate):
    plate = str(plate).strip().upper()

    if not plate:
        return False, "empty_plate"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_plate = vehicle[2] or vehicle[3]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET
            license_plate = ?,
            license_plate_normalized = ?
        WHERE id = ?
    """, (
        plate,
        plate,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_plate,
        "new_value": plate,
    }


def update_vehicle_model(vehicle_id, model):
    model = str(model).strip().upper()

    if not model:
        return False, "empty_model"

    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    old_model = vehicle[4] or vehicle[5]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE vehicles
        SET
            car_model = ?,
            car_model_normalized = ?
        WHERE id = ?
    """, (
        model,
        model,
        int(vehicle_id),
    ))

    changed = cur.rowcount
    conn.commit()
    conn.close()

    if not changed:
        return False, "not_updated"

    return True, {
        "vehicle_id": int(vehicle_id),
        "old_value": old_model,
        "new_value": model,
    }


def get_next_vehicle_for_review():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id,
            a.apartment_number,
            v.license_plate_normalized,
            v.license_plate,
            v.car_model_normalized,
            v.car_model,
            v.parking_time
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        WHERE
            v.parking_time IS NULL
            OR TRIM(v.parking_time) = ''
        ORDER BY
            CASE
                WHEN a.apartment_number GLOB '[0-9]*'
                THEN CAST(a.apartment_number AS INTEGER)
                ELSE 999999
            END,
            a.apartment_number,
            v.id
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()
    return row


def set_vehicle_day(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Day")


def set_vehicle_night(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Night")


def set_vehicle_inactive(vehicle_id):
    return update_vehicle_parking_status(vehicle_id, "Inactive")


def skip_vehicle_review(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)

    if not vehicle:
        return False, "vehicle_not_found"

    return True, {
        "vehicle_id": int(vehicle_id),
        "action": "skipped",
    }


def get_vehicle_review_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vehicles")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Day'")
    day_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Night'")
    night_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM vehicles WHERE parking_time = 'Inactive'")
    inactive_count = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM vehicles
        WHERE parking_time IS NULL
           OR TRIM(parking_time) = ''
    """)
    missing_count = cur.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "Day": day_count,
        "Night": night_count,
        "Inactive": inactive_count,
        "missing": missing_count,
    }


def format_vehicle_review_card(vehicle):
    if not vehicle:
        return "Все автомобили уже имеют статус Day / Night / Inactive."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = vehicle

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        "🚗 Проверка автомобиля\n\n"
        f"ID: {vehicle_id}\n"
        f"Квартира: {apartment_number}\n\n"
        f"Номер: {plate}\n"
        f"Марка: {model}\n"
        f"Статус: {status}\n\n"
        "Выберите действие:"
    )


def get_vehicles_by_status(status_filter="all", limit=50):
    conn = get_conn()
    cur = conn.cursor()

    where = ""

    if status_filter == "missing":
        where = """
        WHERE v.parking_time IS NULL
           OR TRIM(v.parking_time) = ''
        """
    elif status_filter in ["Day", "Night", "Inactive"]:
        where = "WHERE v.parking_time = ?"

    params = []

    if status_filter in ["Day", "Night", "Inactive"]:
        params.append(status_filter)

    params.append(limit)

    cur.execute(f"""
        SELECT
            v.id,
            a.apartment_number,
            v.license_plate_normalized,
            v.license_plate,
            v.car_model_normalized,
            v.car_model,
            v.parking_time
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        {where}
        ORDER BY
            CASE
                WHEN a.apartment_number GLOB '[0-9]*'
                THEN CAST(a.apartment_number AS INTEGER)
                ELSE 999999
            END,
            a.apartment_number,
            v.id
        LIMIT ?
    """, tuple(params))

    rows = cur.fetchall()
    conn.close()
    return rows


def format_vehicle_admin_line(row):
    if not row:
        return "Автомобиль не найден."

    (
        vehicle_id,
        apartment_number,
        plate_norm,
        plate_raw,
        model_norm,
        model_raw,
        parking_time,
    ) = row

    plate = plate_norm or plate_raw or "-"
    model = model_norm or model_raw or "-"
    status = parking_time or "NULL"

    return (
        f"кв.{apartment_number} | "
        f"{plate} | {model} | {status}"
    )


def format_vehicles_admin_list(title, rows):
    count = len(rows)

    lines = [f"🚗 {title}: {count}", ""]

    if not rows:
        lines.append("Список пуст.")
        return "\n".join(lines)

    for row in rows:
        lines.append("• " + format_vehicle_admin_line(row))

    return "\n".join(lines)

# ==========================================================
# Apartment verification / agreement workflow
# ==========================================================

VERIFICATION_STATUSES = {
    "new": "🆕 Не согласована",
    "confirmed": "✅ Согласована",
    "deferred": "⏳ Отложена",
    "conflict": "⚠️ Конфликт",
    "in_progress": "🔄 В работе",   
}


def get_verification_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM apartment_verification")
    total = cur.fetchone()[0]

    result = {
        "total": total,
        "new": 0,
        "confirmed": 0,
        "deferred": 0,
        "conflict": 0,
    }

    cur.execute("""
        SELECT status, COUNT(*)
        FROM apartment_verification
        GROUP BY status
    """)

    for status, count in cur.fetchall():
        result[status] = count

    conn.close()

    result["done"] = result["confirmed"] + result["deferred"] + result["conflict"]
    result["remaining"] = result["new"]
    result["percent"] = round(result["done"] / total * 100, 1) if total else 0

    return result


def format_verification_stats(stats):
    return (
        "🤝 Согласование квартир\n\n"
        f"Всего квартир: {stats['total']}\n\n"
        f"✅ Согласовано: {stats['confirmed']}\n"
        f"⏳ Отложено: {stats['deferred']}\n"
        f"⚠️ Конфликт: {stats['conflict']}\n"
        f"🆕 Осталось: {stats['new']}\n\n"
        f"Готовность: {stats['percent']}%"
    )


def get_apartment_verification_status(apartment_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            av.id,
            av.apartment_id,
            av.apartment_number,
            av.status,
            av.comment,
            av.verified_by,
            av.verified_at,
            av.updated_at
        FROM apartment_verification av
        WHERE av.apartment_number = ?
    """, (str(apartment_number),))

    row = cur.fetchone()
    conn.close()
    return row


def get_next_apartment_for_verification(skip_apartment_numbers=None):
    skip_apartment_numbers = [
        str(x) for x in (skip_apartment_numbers or [])
        if str(x).strip()
    ]

    conn = get_conn()
    cur = conn.cursor()

    params = []
    skip_sql = ""

    if skip_apartment_numbers:
        placeholders = ",".join("?" for _ in skip_apartment_numbers)
        skip_sql = f"AND av.apartment_number NOT IN ({placeholders})"
        params.extend(skip_apartment_numbers)

    cur.execute(f"""
        SELECT
            av.id,
            av.apartment_id,
            av.apartment_number,
            av.status,
            av.comment,
            av.verified_by,
            av.verified_at,
            av.updated_at
        FROM apartment_verification av
        WHERE av.status = 'new'
        {skip_sql}
        ORDER BY
            CASE
                WHEN av.apartment_number GLOB '[0-9]*'
                THEN CAST(av.apartment_number AS INTEGER)
                ELSE 999999
            END,
            av.apartment_number
        LIMIT 1
    """, tuple(params))

    row = cur.fetchone()
    conn.close()
    return row


def get_apartments_by_verification_status(status, limit=30):
    if status not in VERIFICATION_STATUSES:
        return []

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            av.id,
            av.apartment_id,
            av.apartment_number,
            av.status,
            av.comment,
            av.verified_by,
            av.verified_at,
            av.updated_at
        FROM apartment_verification av
        WHERE av.status = ?
        ORDER BY
            CASE
                WHEN av.apartment_number GLOB '[0-9]*'
                THEN CAST(av.apartment_number AS INTEGER)
                ELSE 999999
            END,
            av.apartment_number
        LIMIT ?
    """, (status, int(limit)))

    rows = cur.fetchall()
    conn.close()
    return rows


def set_apartment_verification_status(
    apartment_number,
    status,
    verified_by=None,
    comment=None,
):
    if status not in VERIFICATION_STATUSES:
        return False, "invalid_status"

    apt = find_apartment(apartment_number)

    if not apt:
        return False, "apartment_not_found"

    apartment_id = apt[0]
    apartment_number = str(apt[1])
    verified_at = now() if status in ["confirmed", "deferred", "conflict"] else None

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO apartment_verification (
            apartment_id,
            apartment_number,
            status,
            comment,
            verified_by,
            verified_at,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(apartment_id)
        DO UPDATE SET
            apartment_number = excluded.apartment_number,
            status = excluded.status,
            comment = excluded.comment,
            verified_by = excluded.verified_by,
            verified_at = excluded.verified_at,
            updated_at = excluded.updated_at
    """, (
        apartment_id,
        apartment_number,
        status,
        comment,
        int(verified_by) if verified_by else None,
        verified_at,
        now(),
        now(),
    ))

    conn.commit()
    conn.close()

    return True, status


def format_verification_apartment_list(title, rows):
    lines = [f"🤝 {title}: {len(rows)}", ""]

    if not rows:
        lines.append("Список пуст.")
        return "\n".join(lines)

    for row in rows:
        (
            verification_id,
            apartment_id,
            apartment_number,
            status,
            comment,
            verified_by,
            verified_at,
            updated_at,
        ) = row

        label = VERIFICATION_STATUSES.get(status, status)
        suffix = f" | {comment}" if comment else ""
        lines.append(f"• кв.{apartment_number} | {label}{suffix}")

    return "\n".join(lines)



# ==========================================================
# Telegram bot quarantine source for agreement
# ==========================================================

def get_tbot_source_rows(apartment_number):
    db_file = paths.OSBB_QUARANTINE_DB_FILE

    if not db_file.exists():
        return {
            "ok": False,
            "error": f"quarantine_db_not_found: {db_file}",
            "rows": [],
        }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'tbot_parking_import'
    """)

    if not cur.fetchone():
        conn.close()
        return {
            "ok": False,
            "error": "table_tbot_parking_import_not_found",
            "rows": [],
        }

    cur.execute("PRAGMA table_info(tbot_parking_import)")
    columns = [row[1] for row in cur.fetchall()]

    def pick(*names):
        for name in names:
            if name in columns:
                return name
        return None

    apartment_col = pick("apartment_number", "Номер квартири", "Номер квартиры", "Квартира")
    plate_norm_col = pick("license_plate_normalized")
    plate_raw_col = pick("license_plate", "Номер Авто", "Номер авто", "plate")
    model_norm_col = pick("car_model_normalized")
    model_raw_col = pick("car_model", "Марка авто", "Марка", "model")
    phone_col = pick("phone_normalized", "phone_number", "Телефон", "phone")
    status_col = pick("status", "Статус", "parking_time", "Тариф")

    if not apartment_col:
        conn.close()
        return {
            "ok": False,
            "error": "apartment_column_not_found",
            "rows": [],
        }

    select_parts = [
        f"{apartment_col} AS apartment_number"
    ]

    if plate_norm_col:
        select_parts.append(f"{plate_norm_col} AS license_plate_normalized")
    else:
        select_parts.append("NULL AS license_plate_normalized")

    if plate_raw_col:
        select_parts.append(f"{plate_raw_col} AS license_plate")
    else:
        select_parts.append("NULL AS license_plate")

    if model_norm_col:
        select_parts.append(f"{model_norm_col} AS car_model_normalized")
    else:
        select_parts.append("NULL AS car_model_normalized")

    if model_raw_col:
        select_parts.append(f"{model_raw_col} AS car_model")
    else:
        select_parts.append("NULL AS car_model")

    if phone_col:
        select_parts.append(f"{phone_col} AS phone_normalized")
    else:
        select_parts.append("NULL AS phone_normalized")

    if status_col:
        select_parts.append(f"{status_col} AS status")
    else:
        select_parts.append("NULL AS status")

    sql = f"""
        SELECT
            {", ".join(select_parts)}
        FROM tbot_parking_import
        WHERE CAST({apartment_col} AS TEXT) = ?
        ORDER BY rowid
    """

    cur.execute(sql, (str(apartment_number),))

    rows = cur.fetchall()
    conn.close()

    return {
        "ok": True,
        "error": None,
        "rows": rows,
    }


def format_tbot_source_rows(source):
    lines = ["🤖 Бот"]

    if not source["ok"]:
        lines.append(f"источник недоступен: {source['error']}")
        return "\n".join(lines)

    if not source["rows"]:
        lines.append("нет записей")
        return "\n".join(lines)

    for row in source["rows"]:
        (
            apartment_number,
            plate_norm,
            plate_raw,
            model_norm,
            model_raw,
            phone_norm,
            status,
        ) = row

        plate = plate_norm or plate_raw or "-"
        model = model_norm or model_raw or "-"
        phone = phone_norm or "-"
        status = status or "-"

        lines.append(f"• {plate} | {model} | {phone} | {status}")

    return "\n".join(lines)


def get_main_db_vehicle_rows_for_compare(apartment_number):
    vehicles = get_apartment_vehicles(apartment_number)
    result = []

    for row in vehicles:
        (
            vehicle_id,
            plate_norm,
            plate_raw,
            model_norm,
            model_raw,
            parking_time,
        ) = row

        result.append({
            "plate": plate_norm or plate_raw or "-",
            "model": model_norm or model_raw or "-",
            "parking_time": parking_time or "NULL",
        })

    return result



# ==========================================================
# Telegram message facts source for agreement
# ==========================================================

PARKING_DAY_WORDS = [
    "day",
    "день",
    "денна",
    "днев",
    "денной",
]

PARKING_NIGHT_WORDS = [
    "night",
    "ніч",
    "ноч",
    "ночная",
    "нічна",
]


def detect_parking_time_from_text(text):
    if not text:
        return None

    lower = str(text).lower()

    if any(word in lower for word in PARKING_NIGHT_WORDS):
        return "Night"

    if any(word in lower for word in PARKING_DAY_WORDS):
        return "Day"

    return None


def get_telegram_facts_by_apartment(apartment_number):
    """
    Читает источник из Telegram-сообщений:
    osbb_telegram.db / telegram_facts + telegram_messages.
    """
    db_file = paths.OSBB_TELEGRAM_DB_FILE

    if not db_file.exists():
        return {
            "ok": False,
            "error": f"telegram_db_not_found: {db_file}",
            "rows": [],
        }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'telegram_facts'
    """)

    if not cur.fetchone():
        conn.close()
        return {
            "ok": False,
            "error": "table_telegram_facts_not_found",
            "rows": [],
        }

    cur.execute("""
        SELECT
            f.id,
            f.fact_type,
            f.apartment_number,
            f.person_name,
            f.phone_normalized,
            f.license_plate_normalized,
            f.license_plate,
            f.car_brand,
            f.car_model,
            f.car_color_normalized,
            f.amount,
            f.remote_count,
            f.fact_status,
            f.comment,
            m.text_raw,
            m.message_date,
            m.sender_name
        FROM telegram_facts f
        LEFT JOIN telegram_messages m
            ON m.id = f.telegram_message_db_id
        WHERE CAST(f.apartment_number AS TEXT) = ?
        ORDER BY f.id
    """, (str(apartment_number),))

    raw_rows = cur.fetchall()
    conn.close()

    rows = []

    for row in raw_rows:
        (
            fact_id,
            fact_type,
            apt,
            person_name,
            phone_normalized,
            plate_norm,
            plate_raw,
            car_brand,
            car_model,
            car_color,
            amount,
            remote_count,
            fact_status,
            comment,
            text_raw,
            message_date,
            sender_name,
        ) = row

        parking_hint = (
            detect_parking_time_from_text(fact_type)
            or detect_parking_time_from_text(comment)
            or detect_parking_time_from_text(text_raw)
        )

        rows.append({
            "fact_id": fact_id,
            "fact_type": fact_type,
            "apartment_number": apt,
            "person_name": person_name,
            "phone": phone_normalized,
            "plate": plate_norm or plate_raw,
            "model": " ".join(
                x for x in [car_brand, car_model]
                if x
            ) or None,
            "color": car_color,
            "amount": amount,
            "remote_count": remote_count,
            "fact_status": fact_status,
            "comment": comment,
            "text_raw": text_raw,
            "message_date": message_date,
            "sender_name": sender_name,
            "parking_hint": parking_hint,
        })

    return {
        "ok": True,
        "error": None,
        "rows": rows,
    }


def format_telegram_facts_source_rows(source):
    lines = ["💬 Сообщения"]

    if not source["ok"]:
        lines.append(f"источник недоступен: {source['error']}")
        return "\n".join(lines)

    rows = source["rows"]

    if not rows:
        lines.append("нет фактов")
        return "\n".join(lines)

    for item in rows:
        fact_type = item.get("fact_type") or "-"
        plate = item.get("plate")
        model = item.get("model")
        phone = item.get("phone")
        parking_hint = item.get("parking_hint")
        remote_count = item.get("remote_count")
        amount = item.get("amount")

        parts = []

        if plate:
            parts.append(str(plate))

        if model:
            parts.append(str(model))

        if parking_hint:
            parts.append(f"parking: {parking_hint}")

        if phone:
            parts.append(str(phone))

        if remote_count:
            parts.append(f"пультов: {remote_count}")

        if amount:
            parts.append(f"сумма: {amount}")

        if not parts:
            comment = item.get("comment")
            text_raw = item.get("text_raw")
            if comment:
                parts.append(str(comment)[:80])
            elif text_raw:
                parts.append(str(text_raw).replace("\n", " ")[:80])
            else:
                parts.append(fact_type)

        lines.append("• " + " | ".join(parts))

    return "\n".join(lines)


def get_telegram_message_plates(apartment_number):
    source = get_telegram_facts_by_apartment(apartment_number)

    plates = set()

    if not source["ok"]:
        return plates

    for item in source["rows"]:
        plate = item.get("plate")
        if plate:
            plates.add(str(plate).upper().strip())

    return plates


def get_telegram_parking_hints(apartment_number):
    source = get_telegram_facts_by_apartment(apartment_number)

    hints = []

    if not source["ok"]:
        return hints

    for item in source["rows"]:
        if item.get("parking_hint"):
            plate = item.get("plate") or "-"
            hints.append((plate, item["parking_hint"]))

    return hints



# ==========================================================
# Agreement suggestions and cleaned message facts
# ==========================================================

def normalize_source_plate(value):
    if not value:
        return None
    return str(value).upper().replace(" ", "").strip()


def get_clean_telegram_facts_by_apartment(apartment_number):
    source = get_telegram_facts_by_apartment(apartment_number)

    if not source["ok"]:
        return source

    seen = set()
    cleaned = []

    for item in source["rows"]:
        plate = normalize_source_plate(item.get("plate"))
        parking_hint = item.get("parking_hint")

        compact_key = (
            item.get("apartment_number"),
            plate,
            parking_hint,
            item.get("remote_count"),
            item.get("amount"),
            item.get("text_raw"),
        )

        if compact_key in seen:
            continue

        seen.add(compact_key)

        comment = item.get("comment")
        if plate and comment and "no plate found" in str(comment).lower():
            item = dict(item)
            item["comment"] = None

        cleaned.append(item)

    return {
        "ok": True,
        "error": None,
        "rows": cleaned,
    }


def format_telegram_facts_source_rows(source):
    lines = ["💬 Сообщения"]

    if not source["ok"]:
        lines.append(f"источник недоступен: {source['error']}")
        return "\n".join(lines)

    rows = source["rows"]

    if not rows:
        lines.append("нет фактов")
        return "\n".join(lines)

    for item in rows:
        fact_type = item.get("fact_type") or "-"
        plate = item.get("plate")
        model = item.get("model")
        phone = item.get("phone")
        parking_hint = item.get("parking_hint")
        remote_count = item.get("remote_count")
        amount = item.get("amount")
        comment = item.get("comment")
        text_raw = item.get("text_raw")

        parts = []

        if plate:
            parts.append(str(plate))

        if model:
            parts.append(str(model))

        if parking_hint:
            parts.append(f"parking: {parking_hint}")

        if phone:
            parts.append(str(phone))

        if remote_count:
            parts.append(f"пультов: {remote_count}")

        if amount:
            parts.append(f"сумма: {amount}")

        if comment:
            parts.append(str(comment)[:80])
        elif not parts and text_raw:
            parts.append(str(text_raw).replace("\n", " ")[:80])

        if not parts:
            parts.append(fact_type)

        lines.append("• " + " | ".join(parts))

    return "\n".join(lines)


def build_agreement_suggestion(apartment_number):
    tbot = get_tbot_source_rows(apartment_number)
    msg_source = get_clean_telegram_facts_by_apartment(apartment_number)
    db_rows = get_main_db_vehicle_rows_for_compare(apartment_number)

    candidates = {}

    def ensure(plate):
        plate = normalize_source_plate(plate)
        if not plate:
            return None
        if plate not in candidates:
            candidates[plate] = {
                "plate": plate,
                "sources": set(),
                "models": [],
                "parking_hints": [],
                "phones": [],
            }
        return candidates[plate]

    for item in db_rows:
        c = ensure(item.get("plate"))
        if not c:
            continue
        c["sources"].add("БД")
        if item.get("model") and item.get("model") != "-":
            c["models"].append(str(item["model"]))
        if item.get("parking_time") and item.get("parking_time") != "NULL":
            c["parking_hints"].append(str(item["parking_time"]))

    if tbot["ok"]:
        for row in tbot["rows"]:
            c = ensure(row[1] or row[2])
            if not c:
                continue
            c["sources"].add("Бот")
            model = row[3] or row[4]
            if model:
                c["models"].append(str(model))
            if row[5]:
                c["phones"].append(str(row[5]))
            if row[6]:
                c["parking_hints"].append(str(row[6]))

    if msg_source["ok"]:
        for item in msg_source["rows"]:
            c = ensure(item.get("plate"))
            if not c:
                continue
            c["sources"].add("Сообщения")
            if item.get("model"):
                c["models"].append(str(item["model"]))
            if item.get("phone"):
                c["phones"].append(str(item["phone"]))
            if item.get("parking_hint"):
                c["parking_hints"].append(str(item["parking_hint"]))

    def most_common(values):
        clean = [str(v).strip() for v in values if v and str(v).strip() and str(v).strip() != "-"]
        if not clean:
            return None
        counts = {}
        for value in clean:
            counts[value] = counts.get(value, 0) + 1
        return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[0][0]

    suggestions = []

    for plate, data in candidates.items():
        if len(data["sources"]) < 2:
            continue

        suggestions.append({
            "plate": plate,
            "model": most_common(data["models"]),
            "parking_time": most_common(data["parking_hints"]),
            "phone": most_common(data["phones"]),
            "sources": sorted(data["sources"]),
            "confidence": len(data["sources"]),
        })

    suggestions.sort(key=lambda x: (-x["confidence"], x["plate"]))
    return suggestions


def format_agreement_suggestion(apartment_number):
    suggestions = build_agreement_suggestion(apartment_number)

    lines = ["🟢 Предложение"]

    if not suggestions:
        lines.append("пока нет сильного согласованного варианта")
        return "\n".join(lines)

    for item in suggestions:
        parts = [item["plate"]]

        if item.get("model"):
            parts.append(item["model"])

        if item.get("parking_time"):
            parts.append(item["parking_time"])

        if item.get("phone"):
            parts.append(item["phone"])

        lines.append("• " + " | ".join(parts))
        lines.append("  основание: " + " + ".join(item["sources"]))

    return "\n".join(lines)


def get_agreement_compare_summary(apartment_number):
    tbot = get_tbot_source_rows(apartment_number)
    db_rows = get_main_db_vehicle_rows_for_compare(apartment_number)
    msg_source = get_clean_telegram_facts_by_apartment(apartment_number)

    tbot_plates = set()
    if tbot["ok"]:
        for row in tbot["rows"]:
            plate = row[1] or row[2]
            if plate:
                tbot_plates.add(normalize_source_plate(plate))

    db_plates = set()
    for item in db_rows:
        plate = item["plate"]
        if plate and plate != "-":
            db_plates.add(normalize_source_plate(plate))

    message_plates = set()
    if msg_source["ok"]:
        for item in msg_source["rows"]:
            plate = item.get("plate")
            if plate:
                message_plates.add(normalize_source_plate(plate))

    all_external = tbot_plates | message_plates

    only_tbot = sorted(tbot_plates - db_plates)
    only_messages = sorted(message_plates - db_plates)
    only_db = sorted(db_plates - all_external)
    confirmed = sorted(db_plates & all_external)

    lines = ["🔎 Сравнение"]

    if not tbot["ok"]:
        lines.append("бот-анкета недоступна")

    if not msg_source["ok"]:
        lines.append("сообщения недоступны")

    if not tbot_plates and not message_plates and not db_plates:
        lines.append("нет авто ни в источниках, ни в БД")
        return "\n".join(lines)

    lines.append(f"Совпали с БД: {len(confirmed)}")

    if only_tbot:
        lines.append("Только в боте: " + ", ".join(only_tbot))

    if only_messages:
        lines.append("Только в сообщениях: " + ", ".join(only_messages))

    if only_db:
        lines.append("Только в БД: " + ", ".join(only_db))

    parking_hints = []
    if msg_source["ok"]:
        for item in msg_source["rows"]:
            if item.get("parking_hint"):
                plate = normalize_source_plate(item.get("plate")) or "-"
                value = (plate, item["parking_hint"])
                if value not in parking_hints:
                    parking_hints.append(value)

    if parking_hints:
        hints_text = ", ".join(f"{plate}: {hint}" for plate, hint in parking_hints)
        lines.append("Parking из сообщений: " + hints_text)

    if not only_tbot and not only_messages and not only_db:
        lines.append("Номера авто по источникам совпадают.")

    return "\n".join(lines)


def format_apartment_agreement_card(apartment_number):
    card = get_apartment_card(apartment_number)

    if not card:
        return "Квартира не найдена."

    verification = get_apartment_verification_status(apartment_number)

    if verification:
        status = verification[3]
        comment = verification[4]
    else:
        status = "new"
        comment = None

    status_label = VERIFICATION_STATUSES.get(status, status)
    tbot_source = get_tbot_source_rows(apartment_number)
    telegram_facts_source = get_clean_telegram_facts_by_apartment(apartment_number)

    lines = []
    lines.append(f"🏠 Квартира {card['apartment_number']}")
    lines.append(f"Статус: {status_label}")

    if comment:
        lines.append(f"Комментарий: {comment}")

    lines.append("")
    lines.append(format_tbot_source_rows(tbot_source))

    lines.append("")
    lines.append(format_telegram_facts_source_rows(telegram_facts_source))

    lines.append("")
    lines.append("💾 БД")
    lines.append("Авто:")
    lines.append(format_vehicle_list(card["vehicles"]))

    lines.append("")
    lines.append(get_agreement_compare_summary(apartment_number))

    lines.append("")
    lines.append(format_agreement_suggestion(apartment_number))

    lines.append("")
    lines.append("👥 Жильцы:")
    if card["residents"]:
        for first_name, last_name, username, resident_status in card["residents"]:
            name = " ".join(x for x in [first_name, last_name] if x) or "-"
            username = f"@{username}" if username else "-"
            lines.append(f"• {name} | {username} | {resident_status or '-'}")
    else:
        lines.append("нет пользователей")

    return "\n".join(lines)


def set_apartment_verification_in_progress(apartment_number, verified_by=None):
    current = get_apartment_verification_status(apartment_number)

    if current and current[3] != "new":
        return True, current[3]

    return set_apartment_verification_status(
        apartment_number,
        "in_progress",
        verified_by=verified_by,
    )


# ==========================================================
# Agreement dashboard
# ==========================================================

def _safe_table_exists(db_file, table_name):
    if not db_file.exists():
        return False

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
    """, (table_name,))

    exists = cur.fetchone() is not None
    conn.close()
    return exists


def _get_main_apartment_numbers():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT apartment_number
        FROM apartments
    """)

    result = {
        str(row[0]).strip()
        for row in cur.fetchall()
        if row[0] is not None and str(row[0]).strip()
    }

    conn.close()
    return result


def _get_main_vehicle_plates():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COALESCE(license_plate_normalized, license_plate)
        FROM vehicles
        WHERE COALESCE(license_plate_normalized, license_plate) IS NOT NULL
          AND TRIM(COALESCE(license_plate_normalized, license_plate)) <> ''
    """)

    result = {
        normalize_source_plate(row[0])
        for row in cur.fetchall()
        if normalize_source_plate(row[0])
    }

    conn.close()
    return result


def _get_tbot_dashboard_rows():
    db_file = paths.OSBB_QUARANTINE_DB_FILE

    if not _safe_table_exists(db_file, "tbot_parking_import"):
        return {
            "ok": False,
            "error": "tbot_parking_import_not_found",
            "rows": [],
        }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(tbot_parking_import)")
    columns = [row[1] for row in cur.fetchall()]

    def pick(*names):
        for name in names:
            if name in columns:
                return name
        return None

    apartment_col = pick("apartment_number", "Номер квартири", "Номер квартиры", "Квартира")
    plate_norm_col = pick("license_plate_normalized")
    plate_raw_col = pick("license_plate", "Номер Авто", "Номер авто", "plate")
    model_norm_col = pick("car_model_normalized")
    model_raw_col = pick("car_model", "Марка авто", "Марка", "model")
    phone_col = pick("phone_normalized", "phone_number", "Телефон", "phone")

    if not apartment_col:
        conn.close()
        return {
            "ok": False,
            "error": "apartment_column_not_found",
            "rows": [],
        }

    select_parts = [
        f"{apartment_col} AS apartment_number",
        f"{plate_norm_col} AS license_plate_normalized" if plate_norm_col else "NULL AS license_plate_normalized",
        f"{plate_raw_col} AS license_plate" if plate_raw_col else "NULL AS license_plate",
        f"{model_norm_col} AS car_model_normalized" if model_norm_col else "NULL AS car_model_normalized",
        f"{model_raw_col} AS car_model" if model_raw_col else "NULL AS car_model",
        f"{phone_col} AS phone" if phone_col else "NULL AS phone",
    ]

    cur.execute(f"""
        SELECT {", ".join(select_parts)}
        FROM tbot_parking_import
        ORDER BY rowid
    """)

    rows = []
    for row in cur.fetchall():
        apt, plate_norm, plate_raw, model_norm, model_raw, phone = row
        rows.append({
            "apartment_number": str(apt).strip() if apt is not None else None,
            "plate": normalize_source_plate(plate_norm or plate_raw),
            "model": model_norm or model_raw,
            "phone": phone,
        })

    conn.close()

    return {
        "ok": True,
        "error": None,
        "rows": rows,
    }


def _get_telegram_fact_dashboard_rows():
    db_file = paths.OSBB_TELEGRAM_DB_FILE

    if not _safe_table_exists(db_file, "telegram_facts"):
        return {
            "ok": False,
            "error": "telegram_facts_not_found",
            "rows": [],
        }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            f.apartment_number,
            f.license_plate_normalized,
            f.license_plate,
            f.car_brand,
            f.car_model,
            f.comment,
            m.text_raw
        FROM telegram_facts f
        LEFT JOIN telegram_messages m
            ON m.id = f.telegram_message_db_id
        ORDER BY f.id
    """)

    rows = []

    for row in cur.fetchall():
        apt, plate_norm, plate_raw, car_brand, car_model, comment, text_raw = row
        plate = normalize_source_plate(plate_norm or plate_raw)

        rows.append({
            "apartment_number": str(apt).strip() if apt is not None else None,
            "plate": plate,
            "model": " ".join(x for x in [car_brand, car_model] if x) or None,
            "comment": comment,
            "text_raw": text_raw,
            "parking_hint": (
                detect_parking_time_from_text(comment)
                or detect_parking_time_from_text(text_raw)
            ),
        })

    conn.close()

    return {
        "ok": True,
        "error": None,
        "rows": rows,
    }


def _get_ambiguous_telegram_messages(limit=20):
    db_file = paths.OSBB_TELEGRAM_DB_FILE

    if not _safe_table_exists(db_file, "telegram_messages"):
        return {
            "ok": False,
            "error": "telegram_messages_not_found",
            "count": 0,
            "examples": [],
        }

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            telegram_message_id,
            text_raw
        FROM telegram_messages
        WHERE text_raw IS NOT NULL
          AND TRIM(text_raw) <> ''
    """)

    ambiguous = []

    # грубая, но безопасная эвристика:
    # в одном сообщении есть "кв" и "п/под/подъезд", и минимум два числа.
    apt_word_re = re.compile(r"\bкв\.?\b|квартира", re.IGNORECASE)
    entrance_word_re = re.compile(r"\bп\.?\b|под\.?|подъезд|під'?їзд", re.IGNORECASE)
    number_re = re.compile(r"\d+")

    for msg_db_id, msg_id, text in cur.fetchall():
        if not text:
            continue

        numbers = number_re.findall(text)

        if (
            len(numbers) >= 2
            and apt_word_re.search(text)
            and entrance_word_re.search(text)
        ):
            ambiguous.append({
                "message_db_id": msg_db_id,
                "telegram_message_id": msg_id,
                "text": str(text).replace("\n", " ")[:160],
            })

    conn.close()

    return {
        "ok": True,
        "error": None,
        "count": len(ambiguous),
        "examples": ambiguous[:limit],
    }


def get_agreement_dashboard():
    main_apartments = _get_main_apartment_numbers()
    main_plates = _get_main_vehicle_plates()

    tbot = _get_tbot_dashboard_rows()
    telegram = _get_telegram_fact_dashboard_rows()
    ambiguous = _get_ambiguous_telegram_messages(limit=10)
    verification = get_verification_stats()

    dashboard = {
        "verification": verification,
        "tbot": {
            "ok": tbot["ok"],
            "error": tbot["error"],
            "apartments_not_in_db": [],
            "plates_not_in_db": [],
        },
        "telegram": {
            "ok": telegram["ok"],
            "error": telegram["error"],
            "plates_not_in_db": [],
            "parking_hints": [],
        },
        "ambiguous_messages": ambiguous,
    }

    if tbot["ok"]:
        seen_apts = set()
        seen_plates = set()

        for item in tbot["rows"]:
            apt = item.get("apartment_number")
            plate = item.get("plate")

            if apt and apt not in main_apartments:
                seen_apts.add(apt)

            if plate and plate not in main_plates:
                seen_plates.add((apt or "-", plate, item.get("model"), item.get("phone")))

        dashboard["tbot"]["apartments_not_in_db"] = sorted(seen_apts)
        dashboard["tbot"]["plates_not_in_db"] = sorted(seen_plates)

    if telegram["ok"]:
        seen_plates = set()
        seen_hints = set()

        for item in telegram["rows"]:
            apt = item.get("apartment_number") or "-"
            plate = item.get("plate")

            if plate and plate not in main_plates:
                seen_plates.add((apt, plate, item.get("model")))

            if item.get("parking_hint"):
                seen_hints.add((apt, plate or "-", item["parking_hint"]))

        dashboard["telegram"]["plates_not_in_db"] = sorted(seen_plates)
        dashboard["telegram"]["parking_hints"] = sorted(seen_hints)

    return dashboard


def _format_examples(rows, limit=8):
    if not rows:
        return []

    lines = []
    for row in rows[:limit]:
        if isinstance(row, tuple):
            lines.append("  • " + " | ".join(str(x) for x in row if x))
        else:
            lines.append("  • " + str(row))

    if len(rows) > limit:
        lines.append(f"  … ещё {len(rows) - limit}")

    return lines


def format_agreement_dashboard(data):
    lines = []

    lines.append("📌 Сводка дня")
    lines.append("")

    verification = data["verification"]
    lines.append("🤝 Согласование")
    lines.append(f"• новых квартир: {verification.get('new', 0)}")
    lines.append(f"• согласовано: {verification.get('confirmed', 0)}")
    lines.append(f"• отложено: {verification.get('deferred', 0)}")
    lines.append(f"• конфликтов: {verification.get('conflict', 0)}")
    lines.append("")

    lines.append("🤖 Бот-анкета")
    if not data["tbot"]["ok"]:
        lines.append(f"• источник недоступен: {data['tbot']['error']}")
    else:
        apts = data["tbot"]["apartments_not_in_db"]
        plates = data["tbot"]["plates_not_in_db"]

        lines.append(f"• квартир есть в боте, нет в БД: {len(apts)}")
        lines.append(f"• авто есть в боте, нет в БД: {len(plates)}")

        if plates:
            lines.append("• первые авто к разбору:")
            lines.extend(_format_examples(plates, limit=5))
    lines.append("")

    lines.append("💬 Сообщения")
    if not data["telegram"]["ok"]:
        lines.append(f"• источник недоступен: {data['telegram']['error']}")
    else:
        plates = data["telegram"]["plates_not_in_db"]
        hints = data["telegram"]["parking_hints"]

        lines.append(f"• номеров из сообщений нет в БД: {len(plates)}")
        lines.append(f"• найден parking_time в сообщениях: {len(hints)}")

        if plates:
            lines.append("• первые номера к разбору:")
            lines.extend(_format_examples(plates, limit=5))
    lines.append("")

    lines.append("⚠️ Проверить вручную")
    amb = data["ambiguous_messages"]

    if not amb["ok"]:
        lines.append(f"• источник недоступен: {amb['error']}")
    else:
        lines.append(f"• неоднозначных сообщений: {amb['count']}")

        for item in amb["examples"][:3]:
            lines.append(f"  • msg {item['telegram_message_id']}: {item['text']}")

        if amb["count"] > 3:
            lines.append(f"  … ещё {amb['count'] - 3}")

    return "\n".join(lines)

