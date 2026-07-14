"""
Тест для модели Payment
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from OSBB.core_new.domain.payments import Payment, PaymentSummary


def test_create_payment():
    """Тест: создание платежа"""
    print("\n" + "=" * 60)
    print("💰 ТЕСТ: Payment.create()")
    print("=" * 60)
    
    # ⚠️ ЗАМЕНИТЕ НА СУЩЕСТВУЮЩИЙ НОМЕР КВАРТИРЫ
    test_apartment = "174"
    
    success, result = Payment.create(
        amount=150.00,
        apartment_number=test_apartment,
        service_code='parking',
        payment_method='cash',
        comment='Тестовый платеж',
        operator_id='test_operator'
    )
    
    if success:
        payment_id = result.get('payment_id')
        print(f"   ✅ Платеж создан! ID: {payment_id}")
        
        payment = Payment.get_by_id(payment_id)
        if payment:
            print(f"   Сумма: {payment.amount_display}")
            print(f"   Квартира: {payment.apartment_number}")
            print(f"   Услуга: {payment.service_display}")
            print(f"   Статус: {payment.status_display}")
            
            print("\n📋 Карточка платежа:")
            print("-" * 40)
            print(payment.format_card())
            print("-" * 40)
        else:
            print("   ⚠️ Не удалось загрузить созданный платеж")
        
        return True
    else:
        print(f"   ❌ Ошибка: {result}")
        return False


def test_get_payments_by_apartment():
    """Тест: получение платежей по квартире"""
    print("\n" + "=" * 60)
    print("💰 ТЕСТ: Payment.get_by_apartment()")
    print("=" * 60)
    
    test_apartment = "174"
    
    payments = Payment.get_by_apartment(test_apartment, limit=10)
    
    if payments:
        print(f"   ✅ Найдено платежей: {len(payments)}")
        for p in payments[:3]:
            print(f"      • {p.amount_display} | {p.service_display} | {p.status_display}")
        if len(payments) > 3:
            print(f"      ... и еще {len(payments) - 3} платежей")
        return True
    else:
        print(f"   ⚠️ Платежей для квартиры {test_apartment} не найдено")
        return True


def test_payment_summary():
    """Тест: сводка по платежам"""
    print("\n" + "=" * 60)
    print("💰 ТЕСТ: PaymentSummary")
    print("=" * 60)
    
    payments = Payment.get_by_apartment("174", limit=50)
    
    if not payments:
        print("   ⚠️ Нет платежей для сводки")
        return True
    
    summary = PaymentSummary(payments)
    print("\n" + summary.format_summary())
    
    return True


def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "=" * 60)
    print("🧪 ЗАПУСК ТЕСТОВ PAYMENT")
    print("=" * 60)
    
    results = []
    
    results.append(("create_payment", test_create_payment()))
    results.append(("get_by_apartment", test_get_payments_by_apartment()))
    results.append(("summary", test_payment_summary()))
    
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ТЕСТОВ")
    print("=" * 60)
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"   {status} {name}")
    
    print(f"\n   Успешно: {passed}/{total}")


if __name__ == "__main__":
    run_all_tests()