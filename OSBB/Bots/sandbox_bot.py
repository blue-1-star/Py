"""
Песочница для тестирования новой архитектуры core_new
Запускается отдельно, не влияет на основного бота
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем корень проекта в путь
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Добавляем OSBB/ в путь (чтобы видеть core_new)
OSBB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(OSBB_ROOT))

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==========================================
# ИМПОРТ КОНФИГА И ТОКЕНА (КАК В ОСНОВНОМ БОТЕ)
# ==========================================

from config import paths

# Добавляем путь к секретам
if str(paths.SECRETS_DIR) not in sys.path:
    sys.path.insert(0, str(paths.SECRETS_DIR))

from telegram_osbb import TOKEN

# ==========================================
# ИМПОРТЫ НОВОЙ АРХИТЕКТУРЫ
# ==========================================

from core_new.domain.residents import Resident
from core_new.domain.vehicles import Vehicle, VehicleCandidate
from core_new.domain.apartments import Apartment
from core_new.domain.payments import Payment

# ==========================================
# ВЕРСИЯ И ИНФОРМАЦИЯ
# ==========================================

BOT_VERSION = "0.1.0"
BOT_NAME = "OSBB Sandbox (core_new)"
BOT_DESCRIPTION = "Песочница для тестирования новой архитектуры"

# ==========================================
# МЕНЮ ПЕСОЧНИЦЫ
# ==========================================

MAIN_MENU = [
    ["👤 Мой профиль"],
    ["🚗 Мои авто (NEW)"],
    ["➕ Добавить авто"],
    ["🏠 Квартира"],
    ["💰 Платежи"],
    ["📊 Тест всего"],
]

def main_keyboard():
    return ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)

# ==========================================
# ОБРАБОТЧИКИ
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие с версией"""
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    await update.message.reply_text(
        f"🏗️ {BOT_NAME}\n"
        f"Версия: {BOT_VERSION}\n"
        f"Запущен: {now}\n\n"
        f"{BOT_DESCRIPTION}\n\n"
        f"👤 Пользователь: {user.first_name}\n"
        f"📱 ID: {user.id}\n\n"
        "⚠️ ВНИМАНИЕ:\n"
        "• Это ПЕСОЧНИЦА, не влияет на основного бота\n"
        "• Работает с тестовой БД\n"
        "• Только для тестирования новой архитектуры\n\n"
        "Выберите действие:",
        reply_markup=main_keyboard()
    )

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать профиль жителя (новая модель)"""
    user_id = update.effective_user.id
    
    resident = Resident.get_by_telegram_id(user_id)
    
    if not resident:
        await update.message.reply_text(
            "❌ Пользователь не найден в системе.\n"
            "Нажмите /start в основном боте сначала.",
            reply_markup=main_keyboard()
        )
        return
    
    lines = []
    lines.append("👤 ПРОФИЛЬ (новая модель)")
    lines.append("=" * 30)
    lines.append(f"Имя: {resident.display_name}")
    lines.append(f"Username: {resident.username_display}")
    lines.append(f"Квартира: {resident.apartment_number or '❌ не привязана'}")
    lines.append(f"Статус: {resident.status_display}")
    lines.append(f"Роль: {resident.role_display}")
    
    if resident.has_apartment:
        vehicles = resident.get_vehicles()
        lines.append(f"\n🚗 Автомобилей: {len(vehicles)}")
        for v in vehicles[:3]:
            lines.append(f"  • {v.display_name} | {v.status_display}")
        if len(vehicles) > 3:
            lines.append(f"  ... и еще {len(vehicles) - 3}")
    
    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=main_keyboard()
    )

async def show_vehicles_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать автомобили (новая модель)"""
    user_id = update.effective_user.id
    
    resident = Resident.get_by_telegram_id(user_id)
    
    if not resident or not resident.has_apartment:
        await update.message.reply_text(
            "❌ Сначала привяжите квартиру в основном боте.",
            reply_markup=main_keyboard()
        )
        return
    
    vehicles = Vehicle.get_by_apartment(resident.apartment_number)
    
    if not vehicles:
        await update.message.reply_text(
            f"🏠 Квартира {resident.apartment_number}\n\n"
            "🚗 Автомобилей пока нет.\n\n"
            "Используйте '➕ Добавить авто'",
            reply_markup=main_keyboard()
        )
        return
    
    lines = [f"🏠 Квартира {resident.apartment_number}"]
    lines.append(f"👤 {resident.display_name}")
    lines.append("")
    lines.append("🚗 АВТОМОБИЛИ (новая модель)")
    lines.append("-" * 30)
    
    for v in vehicles:
        lines.append(f"  • {v.display_name}")
        lines.append(f"    Статус: {v.status_display}")
        lines.append("")
    
    lines.append(f"Всего: {len(vehicles)} автомобилей")
    
    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=main_keyboard()
    )

async def add_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начать добавление автомобиля"""
    context.user_data['waiting_for_plate'] = True
    await update.message.reply_text(
        "🚗 ДОБАВЛЕНИЕ АВТОМОБИЛЯ\n\n"
        "Введите номер автомобиля:\n"
        "Например: AA8098MM",
        reply_markup=ReplyKeyboardMarkup([["❌ Отмена"]], resize_keyboard=True)
    )

async def handle_plate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода номера"""
    text = update.message.text.strip()
    
    if text == "❌ Отмена":
        context.user_data.clear()
        await update.message.reply_text("❌ Отменено", reply_markup=main_keyboard())
        return
    
    context.user_data['plate'] = text
    context.user_data['waiting_for_model'] = True
    context.user_data.pop('waiting_for_plate', None)
    
    await update.message.reply_text(
        f"Номер: {text}\n\n"
        "Введите марку автомобиля:\n"
        "Например: Toyota Camry",
        reply_markup=ReplyKeyboardMarkup([["❌ Отмена"]], resize_keyboard=True)
    )

async def handle_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода марки и создание кандидата"""
    text = update.message.text.strip()
    
    if text == "❌ Отмена":
        context.user_data.clear()
        await update.message.reply_text("❌ Отменено", reply_markup=main_keyboard())
        return
    
    plate = context.user_data.get('plate')
    model = text
    user_id = update.effective_user.id
    
    context.user_data.clear()
    
    # Получаем жителя
    resident = Resident.get_by_telegram_id(user_id)
    if not resident or not resident.has_apartment:
        await update.message.reply_text(
            "❌ У вас не привязана квартира.",
            reply_markup=main_keyboard()
        )
        return
    
    # Создаем кандидата
    candidate = VehicleCandidate(plate, model)
    success, result = candidate.approve(resident.apartment_number)
    
    if success:
        vehicle = result
        await update.message.reply_text(
            f"✅ АВТОМОБИЛЬ ДОБАВЛЕН!\n\n"
            f"Номер: {vehicle.plate}\n"
            f"Марка: {vehicle.model}\n"
            f"Квартира: {vehicle.apartment_number}\n"
            f"Статус: {vehicle.status_display}",
            reply_markup=main_keyboard()
        )
    else:
        await update.message.reply_text(
            f"❌ Ошибка: {result}\n\n"
            "Возможно, такой автомобиль уже есть.",
            reply_markup=main_keyboard()
        )

async def show_apartment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать квартиру (новая модель)"""
    user_id = update.effective_user.id
    
    resident = Resident.get_by_telegram_id(user_id)
    if not resident or not resident.has_apartment:
        await update.message.reply_text(
            "❌ Квартира не привязана.",
            reply_markup=main_keyboard()
        )
        return
    
    apartment = Apartment.get_by_number(resident.apartment_number)
    if not apartment:
        await update.message.reply_text(
            f"❌ Квартира {resident.apartment_number} не найдена в БД.",
            reply_markup=main_keyboard()
        )
        return
    
    await update.message.reply_text(
        apartment.format_card(),
        reply_markup=main_keyboard()
    )

async def show_payments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать платежи (новая модель)"""
    user_id = update.effective_user.id
    
    resident = Resident.get_by_telegram_id(user_id)
    if not resident or not resident.has_apartment:
        await update.message.reply_text(
            "❌ Квартира не привязана.",
            reply_markup=main_keyboard()
        )
        return
    
    payments = Payment.get_by_apartment(resident.apartment_number, limit=10)
    
    if not payments:
        await update.message.reply_text(
            f"💰 Платежей для квартиры {resident.apartment_number} нет.",
            reply_markup=main_keyboard()
        )
        return
    
    lines = [f"💰 ПЛАТЕЖИ (новая модель)"]
    lines.append(f"Квартира: {resident.apartment_number}")
    lines.append("-" * 30)
    
    for p in payments[:5]:
        lines.append(f"  • {p.amount_display} | {p.service_display} | {p.status_display}")
    
    if len(payments) > 5:
        lines.append(f"  ... и еще {len(payments) - 5}")
    
    from core_new.domain.payments import PaymentSummary
    summary = PaymentSummary(payments)
    lines.append("")
    lines.append(summary.format_summary())
    
    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=main_keyboard()
    )

async def test_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Тест всех моделей сразу"""
    user_id = update.effective_user.id
    
    lines = []
    lines.append("🧪 ТЕСТ ВСЕХ МОДЕЛЕЙ")
    lines.append("=" * 30)
    
    # 1. Resident
    resident = Resident.get_by_telegram_id(user_id)
    if resident:
        lines.append(f"✅ Resident: {resident.display_name} | {resident.apartment_number or '-'}")
    else:
        lines.append("❌ Resident: не найден")
    
    # 2. Apartment
    if resident and resident.has_apartment:
        apartment = Apartment.get_by_number(resident.apartment_number)
        if apartment:
            lines.append(f"✅ Apartment: {apartment.display_name} | Жильцов: {apartment.residents_count}")
        else:
            lines.append("❌ Apartment: не найдена")
    
    # 3. Vehicle
    if resident and resident.has_apartment:
        vehicles = Vehicle.get_by_apartment(resident.apartment_number)
        lines.append(f"✅ Vehicle: найдено {len(vehicles)} автомобилей")
    
    # 4. Payment
    if resident and resident.has_apartment:
        payments = Payment.get_by_apartment(resident.apartment_number, limit=5)
        lines.append(f"✅ Payment: найдено {len(payments)} платежей")
    
    lines.append("")
    lines.append("🏗️ Все модели работают!")
    
    await update.message.reply_text(
        "\n".join(lines),
        reply_markup=main_keyboard()
    )

# ==========================================
# ОСНОВНОЙ ОБРАБОТЧИК
# ==========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Маршрутизация сообщений"""
    text = update.message.text
    
    if text == "👤 Мой профиль":
        await show_profile(update, context)
    elif text == "🚗 Мои авто (NEW)":
        await show_vehicles_new(update, context)
    elif text == "➕ Добавить авто":
        await add_vehicle(update, context)
    elif text == "🏠 Квартира":
        await show_apartment(update, context)
    elif text == "💰 Платежи":
        await show_payments(update, context)
    elif text == "📊 Тест всего":
        await test_all(update, context)
    elif context.user_data.get('waiting_for_plate'):
        await handle_plate(update, context)
    elif context.user_data.get('waiting_for_model'):
        await handle_model(update, context)
    else:
        await update.message.reply_text(
            "Используйте кнопки меню.",
            reply_markup=main_keyboard()
        )

# ==========================================
# ЗАПУСК
# ==========================================

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 70)
    print(f"   🏗️  {BOT_NAME}")
    print(f"   Версия: {BOT_VERSION}")
    print(f"   Дата запуска: {now}")
    print("=" * 70)
    print(f"   📌 {BOT_DESCRIPTION}")
    print("=" * 70)
    print(f"   📁 Путь к БД: {paths.OSBB_TEST_DB_FILE}")
    print(f"   📁 БД существует: {paths.OSBB_TEST_DB_FILE.exists()}")
    print("=" * 70)
    print(f"   🤖 Токен: {TOKEN[:10]}... (первые 10 символов)")
    print(f"   📱 Бот запущен. Нажмите /start в Telegram")
    print("=" * 70)
    print("   ⚠️  ВНИМАНИЕ: Это ПЕСОЧНИЦА!")
    print("   - Не влияет на основного бота")
    print("   - Работает с тестовой БД")
    print("=" * 70)
    print()
    
    try:
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("🔄 Бот запущен и готов к работе...")
        app.run_polling()
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        print("=" * 70)
        print("Возможные причины:")
        print("  1. Неправильный токен в telegram_osbb.py")
        print("  2. Проблемы с подключением к Telegram API")
        print("  3. Ошибка в коде")
        print("=" * 70)

if __name__ == "__main__":
    main()