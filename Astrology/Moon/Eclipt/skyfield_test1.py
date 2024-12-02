from skyfield.api import load
from datetime import datetime

# Загружаем эфемериды (база DE421, скачивается при первом вызове)
eph = load('de421.bsp')  # DE421 — набор данных JPL, включает Землю и Луну
earth = eph['earth']     # Земля как наблюдатель
moon = eph['moon']       # Луна как целевой объект

def get_moon_coordinates(time):
    ts = load.timescale()  # Создание временной шкалы Skyfield
    t = ts.utc(time.year, time.month, time.day, time.hour, time.minute, time.second)  # Преобразование времени в UTC

    # Получение положения Луны относительно Земли
    astrometric = earth.at(t).observe(moon).apparent()

    # Эклиптические координаты
    ecliptic = astrometric.ecliptic_latlon()
    return {
        "longitude": ecliptic[1].degrees,  # Эклиптическая долгота
        "latitude": ecliptic[0].degrees,   # Эклиптическая широта
        "distance_km": astrometric.distance().km  # Расстояние в километрах
    }

# Пример вызова
time = datetime(2024, 11, 28, 14, 0)  # Дата и время
result = get_moon_coordinates(time)
print(f"Эклиптическая долгота: {result['longitude']}°")
print(f"Эклиптическая широта: {result['latitude']}°")
print(f"Расстояние до Луны: {result['distance_km']} км")
