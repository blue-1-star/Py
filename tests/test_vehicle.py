import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path("G:/Programming/Py")))

from OSBB.core_new.domain.vehicles import Vehicle

print("=" * 60)
print("🚗 Тест новой модели автомобилей")
print("=" * 60)

# 1. Пробуем получить автомобиль по ID
print("\n1️⃣ Получение автомобиля по ID:")
vehicle = Vehicle.get_by_id(1)
if vehicle:
    print(f"   ✅ Автомобиль найден: {vehicle.display_name}")
    print(f"   Статус: {vehicle.status_display}")
else:
    print("   ⚠️ Автомобиль с ID=1 не найден (возможно, его нет в БД)")

# 2. Пробуем получить авто квартиры
print("\n2️⃣ Автомобили квартиры 105:")
vehicles = Vehicle.get_by_apartment("105")
if vehicles:
    for v in vehicles[:5]:
        print(f"   • {v.display_name} | {v.status_display}")
    if len(vehicles) > 5:
        print(f"   ... и еще {len(vehicles) - 5} авто")
else:
    print("   ❌ Квартира 105 не найдена или нет авто")

print("\n" + "=" * 60)
print("✅ Тест завершен!")
print("=" * 60)