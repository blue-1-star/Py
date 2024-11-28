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

def moon_phase_and_day(date):
    from datetime import datetime

    # Константы
    SYNODIC_MONTH = 29.53058867  # Средняя продолжительность лунного месяца
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)  # Известное новолуние

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

    return phase, lunar_day

# Пример использования:
date = datetime(1952, 7, 30)  # Задайте нужную дату
# phase, phase_name = moon_phase(date)
# print(f"Фаза Луны: {phase} (около {phase_name})")
# 
# Задаем текущую дату
current_date = datetime.now()

# Получаем фазу Луны и лунный день
phase, lunar_day = moon_phase_and_day(current_date)

print(f"Фаза Луны: {phase}")
print(f"лунный день: {lunar_day}")

