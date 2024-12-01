# from datetime import datetime
from datetime import datetime, timedelta
import math

def moon_phase(date):
    # Преобразуем дату в формат "год, месяц, день"
    year = date.year
    month = date.month
    day = date.day
    
    # Если месяц январь или февраль, преобразуем в 13 или 14 месяц прошлого года
    if month < 3:
        year -= 1
        month += 12

    # Алгоритм Конвея для вычисления фазы Луны
    k1 = int(365.25 * (year + 4712))
    k2 = int(30.6 * (month + 1))
    k3 = int(((year // 100) + 49) * 0.75) - 38

    # Вычисляем фазу Луны
    julian_day = k1 + k2 + day + 59 - k3
    phase = (julian_day + 1) % 30

    # Определяем название фазы Луны
    if phase == 0:
        phase_name = "Новолуние"
    elif phase < 7:
        phase_name = "Растущий серп"
    elif phase == 15:
        phase_name = "Полнолуние"
    elif phase < 15:
        phase_name = "Первая четверть"
    elif phase < 23:
        phase_name = "Убывающая Луна"
    else:
        phase_name = "Последняя четверть"

    return phase, phase_name



# def moon_phase_and_day(date: datetime):
#     """
#     Определяет фазу Луны и лунный день для указанной даты.
    
#     :param date: Дата, для которой определяется фаза и лунный день (datetime).
#     :return: Кортеж (фаза Луны, лунный день).
#     """
#     # Постоянные значения для расчетов
#     SYNODIC_MONTH = 29.53058867  # Средняя продолжительность синодического месяца (в днях)
#     KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)  # Эпоха нового Луния (UTC)

#     # Разница во времени между указанной датой и известным новолунием
#     delta = (date - KNOWN_NEW_MOON).total_seconds() / (24 * 3600)
    
#     # Номер дня в лунном цикле
#     moon_age = delta % SYNODIC_MONTH
#     lunar_day = int(moon_age) + 1  # Лунный день начинается с 1
#     return phase, lunar_day

# def moon_phase_and_day(date):
#     from datetime import datetime

#     # Константы
#     SYNODIC_MONTH = 29.53058867  # Средняя продолжительность лунного месяца
#     KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)  # Известное новолуние

#     # Разница в днях между заданной датой и известным новолунием
#     delta = (date - KNOWN_NEW_MOON).total_seconds() / (24 * 3600)

#     # Текущая фаза Луны (дробная часть)
#     phase_fraction = (delta % SYNODIC_MONTH) / SYNODIC_MONTH

#     # Лунный день (целая часть)
#     lunar_day = int(phase_fraction * 29.53058867) + 1

#     # Определение текущей фазы Луны
#     if phase_fraction < 0.03 or phase_fraction > 0.97:
#         phase = "New Moon"
#     elif 0.03 <= phase_fraction < 0.25:
#         phase = "Waxing Crescent"
#     elif 0.25 <= phase_fraction < 0.27:
#         phase = "First Quarter"
#     elif 0.27 <= phase_fraction < 0.50:
#         phase = "Waxing Gibbous"
#     elif 0.50 <= phase_fraction < 0.53:
#         phase = "Full Moon"
#     elif 0.53 <= phase_fraction < 0.75:
#         phase = "Waning Gibbous"
#     elif 0.75 <= phase_fraction < 0.77:
#         phase = "Last Quarter"
#     else:
#         phase = "Waning Crescent"

#     return phase, lunar_day
def moon_phase_and_day_with_coordinates(date):
    from datetime import datetime, timedelta
    import math

    # Константы
    SYNODIC_MONTH = 29.53058867  # Средняя продолжительность лунного месяца
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)  # Известное новолуние

    # Средние значения для расчёта эклиптических координат
    MEAN_LONGITUDE_MOON = 218.316  # Средняя долгота Луны (градусы)
    MEAN_ELONGATION = 297.850  # Среднее удаление Луны от Солнца (градусы)
    MEAN_ANOMALY = 134.963  # Средняя аномалия Луны (градусы)
    MEAN_DISTANCE = 93.272  # Среднее расстояние Луны от восходящего узла орбиты (градусы)

    # Разница в днях между заданной датой и известным новолунием
    delta = (date - KNOWN_NEW_MOON).total_seconds() / (24 * 3600)

    # Текущая фаза Луны (дробная часть)
    phase_fraction = (delta % SYNODIC_MONTH) / SYNODIC_MONTH

    # Лунный день (целая часть)
    lunar_day = int(phase_fraction * 29.53058867) + 1

    # Определение текущей фазы Луны
    if phase_fraction < 0.03 or phase_fraction > 0.97:
        phase = "New Moon"
    elif 0.03 <= phase_fraction < 0.25:
        phase = "Waxing Crescent"
    elif 0.25 <= phase_fraction < 0.27:
        phase = "First Quarter"
    elif 0.27 <= phase_fraction < 0.50:
        phase = "Waxing Gibbous"
    elif 0.50 <= phase_fraction < 0.53:
        phase = "Full Moon"
    elif 0.53 <= phase_fraction < 0.75:
        phase = "Waning Gibbous"
    elif 0.75 <= phase_fraction < 0.77:
        phase = "Last Quarter"
    else:
        phase = "Waning Crescent"

    # Расчёт эклиптической долготы Луны (приближённый метод)
    mean_longitude = MEAN_LONGITUDE_MOON + 13.176396 * delta
    mean_anomaly = MEAN_ANOMALY + 13.064993 * delta
    elongation = MEAN_ELONGATION + 12.190749 * delta

# Константы гармоник
    AMP_ANOMALY = 6.289  # Главная поправка аномалии Луны
    AMP_ELONGATION_ANOMALY = -1.274  # Возмущение из-за элонгации и аномалии
    AMP_DOUBLE_ELONGATION = 0.658  # Поправка двойной элонгации
    AMP_DOUBLE_ANOMALY = -0.214  # Поправка двойной аномалии
    AMP_ELONGATION = -0.11  # Поправка элонгации
   
    # Нормализация угла в диапазон [0, 360)
    def normalize_angle(angle):
        return angle % 360

    # Расчёт эклиптической долготы Луны
    longitude = mean_longitude
    longitude += AMP_ANOMALY * math.sin(math.radians(mean_anomaly))
    longitude += AMP_ELONGATION_ANOMALY * math.sin(math.radians(2 * elongation - mean_anomaly))
    longitude += AMP_DOUBLE_ELONGATION * math.sin(math.radians(2 * elongation))
    longitude += AMP_DOUBLE_ANOMALY * math.sin(math.radians(2 * mean_anomaly))
    longitude += AMP_ELONGATION * math.sin(math.radians(elongation))
    longitude = normalize_angle(longitude)


    # longitude = mean_longitude + 6.289 * math.sin(math.radians(mean_anomaly))
    # longitude -= 1.274 * math.sin(math.radians(2 * elongation - mean_anomaly))
    # longitude += 0.658 * math.sin(math.radians(2 * elongation))
    # longitude -= 0.214 * math.sin(math.radians(2 * mean_anomaly))
    # longitude -= 0.11 * math.sin(math.radians(elongation))
    # longitude = longitude % 360

    # Эклиптическая широта
    # Константы для расчётов
    LATITUDE_AMPLITUDE = 5.128  # Максимальная эклиптическая широта Луны (градусы)
    ECCENTRICITY = 0.0549  # Эксцентриситет орбиты Луны
    MEAN_LUNAR_DISTANCE = 385000  # Среднее расстояние от Земли до Луны (км)

    # Эклиптическая широта
    latitude = LATITUDE_AMPLITUDE * math.sin(math.radians(MEAN_DISTANCE))

    # Расстояние до Луны
    distance = MEAN_LUNAR_DISTANCE * (1 - ECCENTRICITY**2) / (
        1 + ECCENTRICITY * math.cos(math.radians(mean_anomaly))
    )


    # latitude = 5.128 * math.sin(math.radians(MEAN_DISTANCE))

    # # Расстояние до Луны
    # eccentricity = 0.0549  # Эксцентриситет орбиты Луны
    # distance = 385000 * (1 - eccentricity**2) / (1 + eccentricity * math.cos(math.radians(mean_anomaly)))

    # Возвращение результатов
    return phase, lunar_day, longitude, latitude, distance



import math

# Наклон эклиптики к экватору (постоянный)
OBLIQUITY = 23.44  # в градусах

def equatorial_to_ecliptic(ra, dec):
    """
    Преобразует экваториальные координаты (RA, Dec) в эклиптические координаты (долгота, широта).
    
    :param ra: Прямое восхождение в часах (часы, минуты, секунды)
    :param dec: Склонение в градусах (градусы, минуты, секунды)
    :return: Эклиптические координаты (долгота, широта) в градусах
    """
    # Перевод RA в градусы
    ra_deg = ra[0] * 15 + ra[1] * 15 / 60 + ra[2] * 15 / 3600
    
    # Перевод Dec в градусы (с учётом знака)
    dec_deg = abs(dec[0]) + dec[1] / 60 + dec[2] / 3600
    if dec[0] < 0:  # если склонение отрицательное
        dec_deg = -dec_deg

    # Преобразование градусов в радианы
    ra_rad = math.radians(ra_deg)
    dec_rad = math.radians(dec_deg)
    obliquity_rad = math.radians(OBLIQUITY)

    # Формулы преобразования
    lambda_rad = math.atan2(
        math.sin(ra_rad) * math.cos(obliquity_rad) + math.tan(dec_rad) * math.sin(obliquity_rad),
        math.cos(ra_rad)
    )
    beta_rad = math.asin(
        math.sin(dec_rad) * math.cos(obliquity_rad) - math.cos(dec_rad) * math.sin(obliquity_rad) * math.sin(ra_rad)
    )

    # Преобразование обратно в градусы
    lambda_deg = math.degrees(lambda_rad)
    beta_deg = math.degrees(beta_rad)

    # Нормализация долготы в диапазон [0, 360)
    if lambda_deg < 0:
        lambda_deg += 360

    return lambda_deg, beta_deg


# Пример использования:
date = datetime(1952, 7, 30)  # Задайте нужную дату
# phase, phase_name = moon_phase(date)
# print(f"Фаза Луны: {phase} (около {phase_name})")
# 
# Задаем текущую дату
current_date = datetime.now()

# Получаем фазу Луны и лунный день
# phase, lunar_day, longitude, latitude = moon_phase_and_day(current_date)
phase, lunar_day, longitude, latitude, distance = moon_phase_and_day_with_coordinates(current_date)
print(f"Фаза Луны: {phase}")
print(f"лунный день: {lunar_day}")
print(f"долгота: {longitude}  широта: {latitude} ")
print(f"distance: {distance}")

# ra = (15, 6, 47.5)  # Прямое восхождение (часы, минуты, секунды)
ra = (15, 9, 52.4)  # Прямое восхождение (часы, минуты, секунды)
# dec = (-21, 54, 12.5)  # Склонение (градусы, минуты, секунды)
dec = (-22, 3, 50)  # Склонение (градусы, минуты, секунды)

longitude_s, latitude_s = equatorial_to_ecliptic(ra, dec)
print(f"Эклиптическая долгота: {longitude_s:.6f}°")
print(f"Эклиптическая широта: {latitude_s:.6f}°")

