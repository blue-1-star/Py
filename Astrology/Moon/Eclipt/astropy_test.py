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
from geopy.geocoders import Nominatim

def get_earth_location(city_name):
    """
    Получает локацию для заданного названия города с использованием geopy.
    Возвращает объект EarthLocation.
    """
    geolocator = Nominatim(user_agent="astropy_location")
    location = geolocator.geocode(city_name)
    if location:
        return EarthLocation(lat=location.latitude, lon=location.longitude, height=0)
    else:
        raise ValueError(f"Город '{city_name}' не найден!")

# Устанавливаем точку наблюдения
# location = EarthLocation.of_site('greenwich')
# Получаем объект локации для Киева
location = get_earth_location("Kyiv")

# Вывод координат
print(f"Координаты для Киева: широта {location.lat}, долгота {location.lon}, высота {location.height}")
if abs(location.height.value) < 1e-3:  # Если высота близка к нулю
    location = EarthLocation(lat=location.lat, lon=location.lon, height=149)  # Установим высоту вручную

# Используем текущее время
time = Time.now()

# Включаем высокоточную эфемериду
with solar_system_ephemeris.set('jpl'):
    moon = get_body("moon", time, location)
    sun = get_sun(time)

# Расстояние до Луны (в AU и км)
distance_au = moon.distance.au  # Расстояние в астрономических единицах
distance_km = distance_au * 149597870.7  # Расстояние в километрах

# Вычисляем угловую фазу Луны (в радианах)
phase_angle = np.arccos(np.dot(
    moon.cartesian.xyz.value / np.linalg.norm(moon.cartesian.xyz.value),
    sun.cartesian.xyz.value / np.linalg.norm(sun.cartesian.xyz.value)
))

# Освещённость Луны
illumination = 0.5 * (1 + np.cos(phase_angle))

# Рассчитаем возраст Луны от последнего новолуния
new_moon_time = Time('2024-12-04T18:32:00')  # Последнее новолуние
age_of_moon = (time - new_moon_time).to_value('day')

# Вывод результатов
print(f"Текущее время: {time.iso}")
print(f"Фаза Луны (освещённость): {illumination:.2f}")
print(f"Возраст Луны (дни от новолуния): {age_of_moon:.2f} дней")
print(f"Расстояние до Луны: {distance_km:.2f} км ({distance_au:.8f} AU)")
print(f"Прямое восхождение: {moon.ra.deg:.2f}°")
print(f"Склонение: {moon.dec.deg:.2f}°")
