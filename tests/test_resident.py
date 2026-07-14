"""
Тест для модели Resident
"""

import sys
from pathlib import Path

# Добавляем путь к проекту
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from OSBB.core_new.domain.residents import Resident


def test_get_resident_by_id():
    """Тест: получение жителя по ID"""
    print("\n" + "=" * 60)
    print("👤 ТЕСТ: Resident.get_by_telegram_id()")
    print("=" * 60)
    
    # ⚠️ ЗАМЕНИТЕ НА СВОЙ TELEGRAM ID!
    test_user_id = 123456789
    
    resident = Resident.get_by_telegram_id(test_user_id)
    
    if resident:
        print(f"   ✅ Найден: {resident.display_name}")
        print(f"   Username: {resident.username_display}")
        print(f"   Квартира: {resident.apartment_number or 'не привязана'}")
        print(f"   Статус: {resident.status_display}")
        print(f"   Роль: {resident.role_display}")
        return True
    else:
        print(f"   ⚠️ Житель с ID {test_user_id} не найден")
        print("   (Это нормально, если вы не запускали бота с этим ID)")
        return False


def test_get_all_residents():
    """Тест: получение всех жителей"""
    print("\n" + "=" * 60)
    print("👤 ТЕСТ: Resident.get_all()")
    print("=" * 60)
    
    residents = Resident.get_all(limit=5)
    
    if residents:
        print(f"   ✅ Найдено жителей: {len(residents)}")
        for r in residents:
            print(f"      • {r.display_name} | {r.apartment_number or '-'} | {r.status_display}")
        return True
    else:
        print("   ⚠️ Жители не найдены")
        return False


def test_get_residents_by_apartment():
    """Тест: получение жителей по квартире"""
    print("\n" + "=" * 60)
    print("👤 ТЕСТ: Resident.get_by_apartment()")
    print("=" * 60)
    
    # ⚠️ ЗАМЕНИТЕ НА СУЩЕСТВУЮЩИЙ НОМЕР КВАРТИРЫ
    test_apartment = "105"
    
    residents = Resident.get_by_apartment(test_apartment)
    
    if residents:
        print(f"   ✅ Квартира {test_apartment}: {len(residents)} жителей")
        for r in residents:
            print(f"      • {r.display_name} | {r.username_display} | {r.status_display}")
        return True
    else:
        print(f"   ⚠️ В квартире {test_apartment} нет жителей")
        print("   (Это нормально, если квартира пустая)")
        return False


def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "=" * 60)
    print("🧪 ЗАПУСК ТЕСТОВ RESIDENT")
    print("=" * 60)
    
    results = []
    
    # Запускаем тесты
    results.append(("get_by_telegram_id", test_get_resident_by_id()))
    results.append(("get_all", test_get_all_residents()))
    results.append(("get_by_apartment", test_get_residents_by_apartment()))
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ТЕСТОВ")
    print("=" * 60)
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "✅" if ok else "❌"
        print(f"   {status} {name}")
    
    print(f"\n   Успешно: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Все тесты пройдены!")
    else:
        print("\n⚠️ Некоторые тесты не пройдены (это нормально, если нет данных в БД)")


if __name__ == "__main__":
    run_all_tests()