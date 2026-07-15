#!/usr/bin/env python
"""
Тест новой кассы (Cashbox) напрямую, минуя бота.
"""

import sys
from pathlib import Path

# Добавляем путь к проекту
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from OSBB.core_new.domain.cashbox import Cashbox
from OSBB.core_new.domain.service_catalog import ServiceCatalog

from config import paths, USE_TEST_DB
print(f"📁 БД: {paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE}")
print(f"📁 Режим: {'ТЕСТОВАЯ' if USE_TEST_DB else 'ОСНОВНАЯ'}")
def main():
    print("=" * 60)
    print("🧪 ТЕСТ НОВОЙ КАССЫ (Cashbox)")
    print("=" * 60)

    # 1. Показываем доступные услуги
    print("\n📋 Доступные услуги:")
    for s in ServiceCatalog.get_all():
        print(f"  {s.code}: {s.name}")

    # 2. Пробуем создать платёж
    print("\n💰 Создаём платёж...")
    result = Cashbox.register_payment(
        amount=500.00,
        plate='8209',
        service_code='PARKING_DAY',
        apartment_number=None,
        payment_method='cash',
        operator_id=12345,
        comment='Тест через консоль'
    )

    print("\n📊 РЕЗУЛЬТАТ:")
    print(f"  success: {result['success']}")
    print(f"  payment_id: {result['payment_id']}")
    print(f"  candidate_id: {result['candidate_id']}")
    print(f"  vehicle_id: {result['vehicle_id']}")
    print(f"  error: {result['error']}")


if __name__ == "__main__":
    main()