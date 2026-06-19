from datetime import datetime
from pathlib import Path
import sqlite3
import sys

from telegram import Update, ReplyKeyboardMarkup

# Put this file here:
#   G:\Programming\Py\OSBB\Bots\handlers\vehicle_verification.py
# It expects this module in OSBB root:
#   G:\Programming\Py\OSBB\vehicle_verification_tasks.py

BOT_HANDLERS_DIR = Path(__file__).resolve().parent
BOTS_DIR = BOT_HANDLERS_DIR.parent
OSBB_ROOT = BOTS_DIR.parent
PY_ROOT = OSBB_ROOT.parent

for p in [str(OSBB_ROOT), str(PY_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import paths, USE_TEST_DB
from vehicle_verification_tasks import (
    get_vehicle_verification_tasks,
    format_vehicle_verification_task,
    normalize_plate,
)


VEHICLE_VERIFICATION_MENU = [
    ["▶️ Начать проверку авто", "📊 Сводка проверки авто"],
    ["⬅️ Назад", "🏠 Главное меню"],
]

TASK_ACTION_MENU = [
    ["✅ Выбрать вариант 1"],
    ["✅ Выбрать вариант 2"],
    ["✅ Выбрать вариант 3"],
    ["✍️ Ввести номер вручную"],
    ["⏭ Пропустить", "📊 Сводка проверки авто"],
    ["⬅️ Назад", "🏠 Главное меню"],
]


def kb(rows):
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def get_db_file():
    return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE


def table_exists(cur, table_name):
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cur.fetchone() is not None


def table_columns(cur, table_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cur.fetchall()]


def insert_operator_audit(
    cur,
    operator_id,
    action_type,
    table_name,
    row_id,
    field_name,
    old_value,
    new_value,
    source_context,
    comment="",
):
    if not table_exists(cur, "operator_audit_log"):
        return

    columns = table_columns(cur, "operator_audit_log")

    values = {
        "operator_id": str(operator_id or ""),
        "user_id": str(operator_id or ""),
        "actor_type": "operator",
        "action_type": action_type,
        "table_name": table_name,
        "row_id": str(row_id or ""),
        "field_name": field_name,
        "old_value": str(old_value or ""),
        "new_value": str(new_value or ""),
        "action_status": "applied",
        "review_status": "pending",
        "source_context": source_context,
        "comment": comment,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    insert_cols = [k for k in values if k in columns]
    if not insert_cols:
        return

    placeholders = ",".join("?" for _ in insert_cols)
    cur.execute(
        f"INSERT INTO operator_audit_log ({', '.join(insert_cols)}) VALUES ({placeholders})",
        tuple(values[k] for k in insert_cols),
    )



def apply_vehicle_plate_correction(
    payment_id,
    vehicle_id,
    operator_id=None,
    comment="vehicle quality correction from bot",
):
    db_file = get_db_file()
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    payments_table = "payments" if table_exists(cur, "payments") else "service_payments"

    if not table_exists(cur, payments_table):
        conn.close()
        raise RuntimeError("payments/service_payments table not found")

    payment_cols = table_columns(cur, payments_table)

    cur.execute("""
        SELECT
            v.id AS vehicle_id,
            a.apartment_number,
            v.parking_time,
            COALESCE(v.license_plate_normalized, v.license_plate) AS plate
        FROM vehicles v
        JOIN apartments a
            ON a.id = v.apartment_id
        WHERE v.id = ?
    """, (vehicle_id,))

    vehicle = cur.fetchone()

    if not vehicle:
        conn.close()
        raise RuntimeError(f"vehicle_id not found: {vehicle_id}")

    service_code = None
    if vehicle["parking_time"] == "Day":
        service_code = "PARKING_DAY"
    elif vehicle["parking_time"] == "Night":
        service_code = "PARKING_NIGHT"

    sets = []
    params = []

    if "vehicle_id" in payment_cols:
        sets.append("vehicle_id = ?")
        params.append(vehicle_id)

    if "apartment_number" in payment_cols:
        sets.append("apartment_number = ?")
        params.append(vehicle["apartment_number"])

    if "service_code" in payment_cols and service_code:
        sets.append("service_code = ?")
        params.append(service_code)

    if "comment" in payment_cols:
        sets.append("comment = COALESCE(comment, '') || ?")
        params.append(
            f"; correction: linked to vehicle_id={vehicle_id}, "
            f"plate={vehicle['plate']}, operator={operator_id}, note={comment}"
        )

    if not sets:
        conn.close()
        raise RuntimeError("payments table has no editable columns")

    params.append(payment_id)

    cur.execute(f"""
        UPDATE {payments_table}
        SET {", ".join(sets)}
        WHERE id = ?
    """, tuple(params))

    updated = cur.rowcount

    insert_operator_audit(
        cur=cur,
        operator_id=operator_id,
        action_type="link_payment_vehicle",
        table_name=payments_table,
        row_id=payment_id,
        field_name="vehicle_id",
        old_value="",
        new_value=str(vehicle_id),
        source_context=f"payment_id={payment_id}; vehicle_id={vehicle_id}; plate={vehicle['plate']}",
        comment=comment,
    )

    conn.commit()
    conn.close()

    return {
        "updated_payments": updated,
        "payment_id": payment_id,
        "vehicle_id": vehicle_id,
        "apartment_number": vehicle["apartment_number"],
        "plate": vehicle["plate"],
        "service_code": service_code,
    }


def update_vehicle_plate_from_source(vehicle_id, new_plate, operator_id=None, source_context="vehicle verification"):
    """
    Operator-controlled action.
    Updates vehicles.license_plate / vehicles.license_plate_normalized.
    It is called only by explicit button: ✏️ N номер источника верный
    """
    db_file = get_db_file()
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, license_plate, license_plate_normalized
        FROM vehicles
        WHERE id = ?
        """,
        (vehicle_id,),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        raise RuntimeError(f"vehicle_id not found: {vehicle_id}")

    old_plate = row["license_plate"] or row["license_plate_normalized"] or ""
    new_plate_norm = normalize_plate(new_plate)

    vehicle_cols = table_columns(cur, "vehicles")
    sets = []
    params = []

    if "license_plate" in vehicle_cols:
        sets.append("license_plate = ?")
        params.append(new_plate_norm)

    if "license_plate_normalized" in vehicle_cols:
        sets.append("license_plate_normalized = ?")
        params.append(new_plate_norm)

    if not sets:
        conn.close()
        raise RuntimeError("vehicles table has no license plate columns")

    params.append(vehicle_id)
    cur.execute(f"UPDATE vehicles SET {', '.join(sets)} WHERE id = ?", tuple(params))

    insert_operator_audit(
        cur=cur,
        operator_id=operator_id,
        action_type="update_vehicle_plate",
        table_name="vehicles",
        row_id=vehicle_id,
        field_name="license_plate",
        old_value=old_plate,
        new_value=new_plate_norm,
        source_context=source_context,
        comment="Vehicle plate corrected from verification task",
    )

    conn.commit()
    conn.close()

    return {"vehicle_id": vehicle_id, "old_plate": old_plate, "new_plate": new_plate_norm}


def get_tasks_cached(user_states, user_id):
    state = user_states.setdefault(user_id, {})
    tasks = state.get("vehicle_verification_tasks")

    if tasks is None:
        tasks = get_vehicle_verification_tasks()
        state["vehicle_verification_tasks"] = tasks
        state["vehicle_verification_index"] = 0

    return tasks


def current_task(user_states, user_id):
    state = user_states.setdefault(user_id, {})
    tasks = get_tasks_cached(user_states, user_id)

    if not tasks:
        return None, 0, 0

    idx = state.get("vehicle_verification_index", 0)
    idx = max(0, min(idx, len(tasks) - 1))
    state["vehicle_verification_index"] = idx
    return tasks[idx], idx, len(tasks)


def recount_vehicle_verification_tasks(user_states, user_id):
    """
    Rebuild task list after applying a correction.
    Returns: old_count, new_count, resolved_count.
    """
    state = user_states.setdefault(user_id, {})
    old_count = len(state.get("vehicle_verification_tasks") or [])

    new_tasks = get_vehicle_verification_tasks()
    new_count = len(new_tasks)

    state["vehicle_verification_tasks"] = new_tasks
    state["vehicle_verification_index"] = 0

    return old_count, new_count, max(0, old_count - new_count)


def format_dashboard(tasks):
    with_candidates = sum(1 for t in tasks if t.get("candidates"))
    without_candidates = len(tasks) - with_candidates

    by_source = {}
    for task in tasks:
        source = task.get("source") or "-"
        by_source[source] = by_source.get(source, 0) + 1

    lines = [
        "🚗 Проверка авто",
        "",
        f"Всего задач: {len(tasks)}",
        f"С кандидатами: {with_candidates}",
        f"Без кандидатов: {without_candidates}",
        "",
    ]

    if by_source:
        lines.append("По источникам:")
        for source, count in sorted(by_source.items()):
            lines.append(f"• {source}: {count}")
        lines.append("")

    lines.append("Нажмите ▶️ Начать проверку авто")
    return "\n".join(lines)


async def show_vehicle_verification_dashboard(update: Update, user_states=None, user_id=None):
    if user_states is None:
        user_states = {}
    if user_id is None:
        user_id = update.effective_user.id if update.effective_user else 0

    state = user_states.setdefault(user_id, {})
    state["vehicle_verification_tasks"] = get_vehicle_verification_tasks()
    state["vehicle_verification_index"] = 0
    state["mode"] = "vehicle_verification"

    await update.message.reply_text(
        format_dashboard(state["vehicle_verification_tasks"]),
        reply_markup=kb(VEHICLE_VERIFICATION_MENU),
    )


async def show_current_vehicle_task(update: Update, user_states, user_id):
    task, idx, total = current_task(user_states, user_id)

    if not task:
        await update.message.reply_text("Задач проверки авто нет.", reply_markup=kb(VEHICLE_VERIFICATION_MENU))
        return

    await update.message.reply_text(
        format_vehicle_verification_task(task, idx + 1, total),
        reply_markup=kb(TASK_ACTION_MENU),
    )


def parse_candidate_index(text):
    for n in range(1, 10):
        if f" {n}" in text or text.strip().endswith(str(n)):
            return n - 1
    return None


async def confirm_same_vehicle(update: Update, user_states, user_id, candidate_index):
    task, idx, total = current_task(user_states, user_id)

    if not task:
        await update.message.reply_text("Нет текущей задачи.")
        return

    candidates = task.get("candidates") or []
    if candidate_index is None or candidate_index < 0 or candidate_index >= len(candidates):
        await update.message.reply_text("Такого кандидата нет в текущей задаче.")
        return

    candidate = candidates[candidate_index]
    payment_id = task.get("payment_id")
    vehicle_id = candidate.get("vehicle_id")

    if payment_id:
        result = apply_vehicle_plate_correction(
            payment_id=payment_id,
            vehicle_id=vehicle_id,
            operator_id=user_id,
            comment="confirmed same vehicle from Telegram bot",
        )
        message = (
            "✅ Оплата привязана к авто.\n\n"
            f"payment_id: {result['payment_id']}\n"
            f"vehicle_id: {result['vehicle_id']}\n"
            f"квартира: {result['apartment_number']}\n"
            f"номер: {result['plate']}"
        )
    else:
        db_file = get_db_file()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        insert_operator_audit(
            cur=cur,
            operator_id=user_id,
            action_type="confirm_same_vehicle",
            table_name="vehicles",
            row_id=vehicle_id,
            field_name="license_plate",
            old_value=candidate.get("plate"),
            new_value=task.get("plate"),
            source_context=(
                f"source={task.get('source')}; source_plate={task.get('plate')}; "
                f"candidate_plate={candidate.get('plate')}; apt={candidate.get('apartment_number')}"
            ),
            comment="Operator confirmed same vehicle; no plate update was applied",
        )
        conn.commit()
        conn.close()
        message = "✅ Подтверждено: это тот же автомобиль.\n\nНомер в базе пока НЕ изменён. Для изменения номера используйте кнопку ✏️."

    user_states.setdefault(user_id, {})["vehicle_verification_index"] = idx + 1
    await update.message.reply_text(message)
    await show_current_vehicle_task(update, user_states, user_id)


async def update_plate_from_candidate(update: Update, user_states, user_id, candidate_index):
    task, idx, total = current_task(user_states, user_id)

    if not task:
        await update.message.reply_text("Нет текущей задачи.")
        return

    candidates = task.get("candidates") or []
    if candidate_index is None or candidate_index < 0 or candidate_index >= len(candidates):
        await update.message.reply_text("Такого кандидата нет в текущей задаче.")
        return

    candidate = candidates[candidate_index]
    source_plate = task.get("plate")

    result = update_vehicle_plate_from_source(
        vehicle_id=candidate["vehicle_id"],
        new_plate=source_plate,
        operator_id=user_id,
        source_context=(
            f"source={task.get('source')}; source_plate={task.get('plate')}; "
            f"source_raw={task.get('plate_raw')}; candidate_plate={candidate.get('plate')}; "
            f"payment_id={task.get('payment_id') or ''}"
        ),
    )

    payment_id = task.get("payment_id")
    if payment_id:
        apply_vehicle_plate_correction(
            payment_id=payment_id,
            vehicle_id=candidate["vehicle_id"],
            operator_id=user_id,
            comment="vehicle plate corrected and payment linked",
        )

    user_states.setdefault(user_id, {})["vehicle_verification_index"] = idx + 1

    await update.message.reply_text(
        "✏️ Номер авто обновлён.\n\n"
        f"vehicle_id: {result['vehicle_id']}\n"
        f"было: {result['old_plate']}\n"
        f"стало: {result['new_plate']}"
    )
    await show_current_vehicle_task(update, user_states, user_id)


async def skip_task(update: Update, user_states, user_id):
    task, idx, total = current_task(user_states, user_id)
    user_states.setdefault(user_id, {})["vehicle_verification_index"] = idx + 1
    await show_current_vehicle_task(update, user_states, user_id)


async def handle_vehicle_verification_text(update: Update, user_states, user_id, text):
    """
    Return True if text was handled here.
    Connect from parking_bot.py message_handler before fallback handling.
    """
    normalized = (text or "").strip()

    if normalized in {"🚗 Проверка авто", "🚗 Верификация авто"}:
        await show_vehicle_verification_dashboard(update, user_states, user_id)
        return True

    state = user_states.setdefault(user_id, {})
    in_mode = state.get("mode") == "vehicle_verification"

    if not in_mode and normalized not in {"▶️ Начать проверку авто", "📊 Сводка проверки авто"}:
        return False

    if normalized == "📊 Сводка проверки авто":
        await show_vehicle_verification_dashboard(update, user_states, user_id)
        return True

    if normalized == "▶️ Начать проверку авто":
        state["mode"] = "vehicle_verification"
        await show_current_vehicle_task(update, user_states, user_id)
        return True

    if normalized == "⏭ Пропустить":
        await skip_task(update, user_states, user_id)
        return True

    if normalized.startswith("✅"):
        await confirm_same_vehicle(update, user_states, user_id, parse_candidate_index(normalized))
        return True

    if normalized.startswith("✏️"):
        await update_plate_from_candidate(update, user_states, user_id, parse_candidate_index(normalized))
        return True

    return False
