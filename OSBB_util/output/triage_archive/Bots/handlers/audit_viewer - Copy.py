from pathlib import Path
import sqlite3
import sys

from telegram import Update, ReplyKeyboardMarkup

BOT_HANDLERS_DIR = Path(__file__).resolve().parent
BOTS_DIR = BOT_HANDLERS_DIR.parent
OSBB_ROOT = BOTS_DIR.parent
PY_ROOT = OSBB_ROOT.parent

for p in [str(OSBB_ROOT), str(PY_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import paths, USE_TEST_DB

AUDIT_MENU = [
    ["🕘 Последние правки"],
    ["👤 Правки операторов", "⚙️ Системные правки"],
    ["⬅️ Назад", "🏠 Главное меню"],
]


def kb(rows):
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def get_db_file():
    return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE


def get_conn():
    conn = sqlite3.connect(get_db_file())
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(cur, table_name):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None


def safe(value):
    return "" if value is None else str(value)


def load_audit(limit=30, actor_filter=None):
    conn = get_conn()
    cur = conn.cursor()

    if not table_exists(cur, "operator_audit_log"):
        conn.close()
        return []

    where = []
    params = []

    if actor_filter:
        where.append("actor_type = ?")
        params.append(actor_filter)

    where_sql = "WHERE " + " AND ".join(where) if where else ""
    params.append(limit)

    cur.execute(f"""
        SELECT
            id,
            created_at,
            actor_type,
            operator_id,
            user_id,
            action_type,
            table_name,
            row_id,
            field_name,
            old_value,
            new_value,
            action_status,
            review_status,
            source_context,
            comment
        FROM operator_audit_log
        {where_sql}
        ORDER BY id DESC
        LIMIT ?
    """, tuple(params))

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


def format_audit_row(row, index):
    old_value = safe(row.get("old_value")) or "∅"
    new_value = safe(row.get("new_value")) or "∅"

    operator = safe(row.get("operator_id")) or safe(row.get("user_id")) or "-"
    actor = safe(row.get("actor_type")) or "-"
    action = safe(row.get("action_type")) or "-"
    table = safe(row.get("table_name")) or "-"
    record_id = safe(row.get("row_id")) or "-"
    field = safe(row.get("field_name")) or "-"
    created = safe(row.get("created_at")) or "-"
    review = safe(row.get("review_status")) or "-"
    comment = safe(row.get("comment"))

    lines = [
        f"{index}. {created}",
        f"   {actor} | {operator}",
        f"   {action}",
        f"   {table} #{record_id} | {field}",
        f"   {old_value} → {new_value}",
        f"   проверка: {review}",
    ]

    if comment:
        lines.append(f"   {comment}")

    lines.append(f"   audit_id={row.get('id')}")

    return "\n".join(lines)


def format_audit_list(rows, title):
    lines = [
        f"🧾 {title}",
        "",
        f"База: {'TEST/WORK' if USE_TEST_DB else 'PROD'}",
        "Источник: operator_audit_log",
        f"Показано: {len(rows)}",
        "",
    ]

    if not rows:
        lines.append("Записей нет.")
        return "\n".join(lines)

    for idx, row in enumerate(rows, start=1):
        lines.append(format_audit_row(row, idx))
        lines.append("")

    return "\n".join(lines)


def split_text(text, limit=3500):
    parts = []
    current = []

    for line in text.splitlines():
        candidate = "\n".join(current + [line])
        if len(candidate) > limit and current:
            parts.append("\n".join(current))
            current = [line]
        else:
            current.append(line)

    if current:
        parts.append("\n".join(current))

    return parts


async def send_long_text(update: Update, text, reply_markup=None):
    parts = split_text(text)

    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            await update.message.reply_text(part, reply_markup=reply_markup)
        else:
            await update.message.reply_text(part)


async def show_audit_dashboard(update: Update, user_states, user_id):
    state = user_states.setdefault(user_id, {})
    state["mode"] = "audit_viewer"

    await update.message.reply_text(
        "🧾 Журнал действий\n\n"
        "Основной журнал: operator_audit_log.\n\n"
        "Здесь видны системные, админские и операторские изменения:\n"
        "• кто изменил\n"
        "• что изменил\n"
        "• было / стало\n"
        "• где изменено\n\n"
        "Выберите режим просмотра.",
        reply_markup=kb(AUDIT_MENU),
    )


async def show_recent_audit(update: Update, actor_filter=None, title="Последние правки"):
    rows = load_audit(limit=30, actor_filter=actor_filter)
    await send_long_text(
        update,
        format_audit_list(rows, title),
        reply_markup=kb(AUDIT_MENU),
    )


async def handle_audit_viewer_text(update: Update, user_states, user_id, text):
    normalized = (text or "").strip()
    state = user_states.setdefault(user_id, {})
    mode = state.get("mode")

    if normalized in {"🧾 Журнал действий", "🧾 Аудит", "👁 Правки операторов"}:
        await show_audit_dashboard(update, user_states, user_id)
        return True

    if mode == "audit_viewer" or normalized in {
        "🕘 Последние правки",
        "👤 Правки операторов",
        "⚙️ Системные правки",
    }:
        if normalized == "🕘 Последние правки":
            await show_recent_audit(update, None, "Последние правки")
            return True

        if normalized == "👤 Правки операторов":
            await show_recent_audit(update, "operator", "Правки операторов")
            return True

        if normalized == "⚙️ Системные правки":
            await show_recent_audit(update, "system", "Системные правки")
            return True

        if normalized in {"⬅️ Назад", "🏠 Главное меню"}:
            state["mode"] = ""
            return False

    return False
