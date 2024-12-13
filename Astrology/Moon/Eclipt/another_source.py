from astropy.coordinates import get_body, EarthLocation
from astropy.time import Time

# Указываем местоположение наблюдателя (например, Гринвич)
location = EarthLocation.of_site('greenwich')

# Указываем время наблюдения
time = Time('2024-12-11T00:00:00')

# Получаем координаты Луны
moon = get_body('moon', time, location)

# Выводим расстояние, прямое восхождение и склонение
print(f"Расстояние до Луны: {moon.distance}")
print(f"Прямое восхождение: {moon.ra}")
print(f"Склонение: {moon.dec}")
#  -----------------
from astropy.coordinates import get_body, get_sun, EarthLocation
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
import numpy as np

# Устанавливаем точку наблюдения и время
location = EarthLocation.of_site('greenwich')
# time = Time('2024-12-11T00:00:00')
time = Time.now()

# Включаем высокоточную эфемериду
with solar_system_ephemeris.set('jpl'):
    moon = get_body("moon", time, location)
    sun = get_sun(time)

# Вычисляем угловую фазу Луны (в радианах)
phase_angle = np.arccos(np.dot(
    moon.cartesian.xyz.value / np.linalg.norm(moon.cartesian.xyz.value),
    sun.cartesian.xyz.value / np.linalg.norm(sun.cartesian.xyz.value)
))

# Освещённость Луны (0 = новолуние, 1 = полнолуние)
illumination = 0.5 * (1 + np.cos(phase_angle))

# Расчёт возраста Луны
# Начало лунного месяца = предыдущее новолуние
# new_moon_time = Time('2024-12-03T00:00:00')  # Пример даты новолуния
new_moon_time = Time('2024-12-04T18:32:00')  # Дата последнего новолуния
age_of_moon = (time - new_moon_time).to_value('day')

# Вывод результатов
print(f"Текущее время: {time.iso}")
print(f"Фаза Луны (освещённость): {illumination:.2f}")
print(f"Возраст Луны (дни от новолуния): {age_of_moon:.2f} дней")
