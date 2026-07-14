"""
Тест для модели Apartment
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from OSBB.core_new.domain.apartments import Apartment


def test_get_apartment_by_number():
    """Тест: получение квартиры по номеру"""
    print("\n" + "=" * 60)
    print("🏠 ТЕСТ: Apartment.get_by_number()")
    print("=" * 60)
    
    # ⚠️ ЗАМЕНИТЕ НА СУЩЕСТВУЮЩИЙ НОМЕР КВАРТИРЫ
    test_apartment = "174"
    
    apartment = Apartment.get_by_number(test_apartment)
    
    if apartment:
        print(f"   ✅ Найдена: {apartment.display_name}")
        print(f"   👥 Жильцы: {apartment.residents_count}")
        print(f"   🚗 Авто: {apartment.vehicles_count}")
        print(f"   📊 Статус: {apartment.verification_status_display}")
        
        # Показываем карточку
        print("\n📋 Карточка квартиры:")
        print("-" * 40)
        print(apartment.format_card())
        print("-" * 40)
        
        return True
    else:
        print(f"   ⚠️ Квартира {test_apartment} не найдена")
        return False


def test_get_all_apartments():
    """Тест: получение всех квартир"""
    print("\n" + "=" * 60)
    print("🏠 ТЕСТ: Apartment.get_all()")
    print("=" * 60)
    
    apartments = Apartment.get_all(limit=10)
    
    if apartments:
        print(f"   ✅ Найдено квартир: {len(apartments)}")
        for a in apartments[:5]:
            print(f"      • {a.display_name}")
        if len(apartments) > 5:
            print(f"      ... и еще {len(apartments) - 5} квартир")
        return True
    else:
        print("   ⚠️ Квартиры не найдены")
        return False


def test_get_apartments_by_entrance():
    """Тест: получение квартир по подъезду"""
    print("\n" + "=" * 60)
    print("🏠 ТЕСТ: Apartment.get_by_entrance()")
    print("=" * 60)
    
    # ⚠️ ЗАМЕНИТЕ НА СУЩЕСТВУЮЩИЙ НОМЕР ПОДЪЕЗДА
    test_entrance = "1"
    
    apartments = Apartment.get_by_entrance(test_entrance)
    
    if apartments:
        print(f"   ✅ Подъезд {test_entrance}: {len(apartments)} квартир")
        for a in apartments[:5]:
            print(f"      • {a.display_name}")
        if len(apartments) > 5:
            print(f"      ... и еще {len(apartments) - 5} квартир")
        return True
    else:
        print(f"   ⚠️ В подъезде {test_entrance} нет квартир")
        return False


def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "=" * 60)
    print("🧪 ЗАПУСК ТЕСТОВ APARTMENT")
    print("=" * 60)
    
    results = []
    
    results.append(("get_by_number", test_get_apartment_by_number()))
    results.append(("get_all", test_get_all_apartments()))
    results.append(("get_by_entrance", test_get_apartments_by_entrance()))
    
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