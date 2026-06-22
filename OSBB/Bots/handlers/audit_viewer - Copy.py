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


def load_new_audit(cur, limit=50, actor_filter=None):
    if not table_exists(cur, "operator_audit_log"):
        return []

    where = ""
    params = []

    if actor_filter:
        where = "WHERE actor_type = ?"
        params.append(actor_filter)

    params.append(limit)

    cur.execute(f"""
        SELECT
            'operator_audit_log' AS source_table,
            id,
            created_at AS event_time,
            actor_type,
            operator_id AS actor_id,
            action_type AS action,
            table_name,
            row_id AS record_id,
            field_name,
            old_value,
            new_value,
            comment
        FROM operator_audit_log
        {where}
        ORDER BY id DESC
        LIMIT ?
    """, tuple(params))

    return [dict(row) for row in cur.fetchall()]


def load_old_audit(cur, limit=50, actor_filter=None):
    if not table_exists(cur, "audit_log"):
        return []

    where = ""
    params = []

    if actor_filter:
        where = "WHERE actor_role = ?"
        params.append(actor_filter)

    params.append(limit)

    cur.execute(f"""
        SELECT
            'audit_log' AS source_table,
            id,
            event_time,
            actor_role AS actor_type,
            COALESCE(CAST(telegram_user_id AS TEXT), username, actor_name, '') AS actor_id,
            action,
            table_name,
            record_id,
            field_name,
            old_value,
            new_value,
            comment
        FROM audit_log
        {where}
        ORDER BY id DESC
        LIMIT ?
    """, tuple(params))

    return [dict(row) for row in cur.fetchall()]


def normalize_row(row):
    return {
        "source_table": safe(row.get("source_table")),
        "id": row.get("id"),
        "event_time": safe(row.get("event_time")),
        "actor_type": safe(row.get("actor_type")) or "-",
        "actor_id": safe(row.get("actor_id")) or "-",
        "action": safe(row.get("action")) or "-",
        "table_name": safe(row.get("table_name")) or "-",
        "record_id": safe(row.get("record_id")) or "-",
        "field_name": safe(row.get("field_name")) or "-",
        "old_value": safe(row.get("old_value")),
        "new_value": safe(row.get("new_value")),
        "comment": safe(row.get("comment")),
    }


def load_unified_audit(limit=30, actor_filter=None):
    conn = get_conn()
    cur = conn.cursor()
    rows = []
    rows.extend(load_new_audit(cur, limit=limit, actor_filter=actor_filter))
    rows.extend(load_old_audit(cur, limit=limit, actor_filter=actor_filter))
    conn.close()

    normalized = [normalize_row(row) for row in rows]
    normalized.sort(key=lambda r: (r["event_time"], int(r["id"] or 0)), reverse=True)
    return normalized[:limit]


def format_audit_row(row, index):
    old_value = row["old_value"] if row["old_value"] != "" else "∅"
    new_value = row["new_value"] if row["new_value"] != "" else "∅"

    lines = [
        f"{index}. {row['event_time'] or '-'}",
        f"   {row['actor_type']} | {row['actor_id']}",
        f"   {row['action']}",
        f"   {row['table_name']} #{row['record_id']} | {row['field_name']}",
        f"   {old_value} → {new_value}",
    ]

    if row["comment"]:
        lines.append(f"   {row['comment']}")

    lines.append(f"   источник: {row['source_table']} id={row['id']}")
    return "\n".join(lines)


def format_audit_list(rows, title):
    lines = [
        f"🧾 {title}",
        "",
        f"База: {'TEST/WORK' if USE_TEST_DB else 'PROD'}",
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
        "Показываются записи из двух таблиц:\n"
        "• operator_audit_log\n"
        "• audit_log\n\n"
        "Выберите режим просмотра.",
        reply_markup=kb(AUDIT_MENU),
    )


async def show_recent_audit(update: Update, actor_filter=None, title="Последние правки"):
    rows = load_unified_audit(limit=30, actor_filter=actor_filter)
    await send_long_text(update, format_audit_list(rows, title), reply_markup=kb(AUDIT_MENU))


async def handle_audit_viewer_text(update: Update, user_states, user_id, text):
    normalized = (text or "").strip()
    state = user_states.setdefault(user_id, {})
    mode = state.get("mode")

    if normalized in {"🧾 Журнал действий", "🧾 Аудит", "👁 Правки операторов"}:
        await show_audit_dashboard(update, user_states, user_id)
        return True

    if mode == "audit_viewer" or normalized in {"🕘 Последние правки", "👤 Правки операторов", "⚙️ Системные правки"}:
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
