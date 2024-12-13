# def julian_date(year, month, day, hour=0, minute=0, second=0, timezone_offset=0):
#     """
#     Вычисляет Юлианскую дату (JD) для произвольной календарной даты нашей эры с учетом местного времени.

#     Параметры:
#         year (int): Год.
#         month (int): Месяц (1–12).
#         day (int): День месяца.
#         hour (int): Часы (0–23).
#         minute (int): Минуты (0–59).
#         second (int): Секунды (0–59).
#         timezone_offset (float): Смещение локального времени относительно UTC (например, +3 для Москвы).

#     Возвращает:
#         float: Юлианская дата, если дата корректна.
#         str: Сообщение, если дата находится в переходном периоде.
#     """
#     # Коррекция времени на UTC
#     hour -= timezone_offset
#     if hour < 0 or hour >= 24:
#         # Обработка перехода на предыдущий или следующий день
#         day += hour // 24
#         hour %= 24
#         if hour < 0:
#             hour += 24
#             day -= 1

#         # Корректировка месяца и года при изменении дня
#         if day < 1:
#             month -= 1
#             if month < 1:
#                 month = 12
#                 year -= 1
#             # Найти количество дней в предыдущем месяце
#             if month in [1, 3, 5, 7, 8, 10, 12]:
#                 day += 31
#             elif month in [4, 6, 9, 11]:
#                 day += 30
#             elif month == 2:
#                 day += 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28

#         elif month > 12:
#             month = 1
#             year += 1

#     # Преобразование времени в дробный день
#     day_fraction = (hour + minute / 60 + second / 3600) / 24

#     # Корректировка для месяцев январь и февраль
#     if month <= 2:
#         year -= 1
#         month += 12

#     # Определение, используется ли Григорианский календарь
#     if (year > 1582) or (year == 1582 and month > 10) or (year == 1582 and month == 10 and day >= 15):
#         # Григорианский календарь
#         A = year // 100
#         B = 2 - A + A // 4
#     elif (year < 1582) or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day <= 4):
#         # Юлианский календарь
#         B = 0
#     else:
#         return "Дата находится в переходном периоде между календарями (5–14 октября 1582 года)."

#     # Вычисление Юлианской даты
#     JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + day_fraction + B - 1524.5
#     return JD
from datetime import datetime
from zoneinfo import ZoneInfo

def julian_date_with_tz(year, month, day, hour=0, minute=0, second=0, timezone='UTC'):
    # Локальное время
    local_time = datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo(timezone))
    
    # Преобразование в UTC

    utc_time = local_time.astimezone(ZoneInfo('UTC'))
    
    # Расчет Юлианской даты
    julian_date = (utc_time - datetime(2000, 1, 1, 12, tzinfo=ZoneInfo('UTC'))).total_seconds() / 86400.0 + 2451545.0
    
    return julian_date

# Пример использования
# print(julian_date_with_tz(2024, 12, 8, 20, 28, 48, timezone='Europe/Moscow'))
# print(julian_date_with_tz(1582, 10, 4, timezone='Europe/Moscow'))


from datetime import datetime
from zoneinfo import ZoneInfo

def julian_date(year, month, day, hour=0, minute=0, second=0, timezone='UTC'):
    """
    Вычисляет Юлианскую дату (JD) с учётом временной зоны и возможного перехода на летнее время.
    
    Аргументы:
        year (int): Год.
        month (int): Месяц.
        day (int): День.
        hour (int, optional): Часы (по умолчанию 0).
        minute (int, optional): Минуты (по умолчанию 0).
        second (int, optional): Секунды (по умолчанию 0).
        timezone (str, optional): Название временной зоны (например, 'Europe/Moscow', по умолчанию 'UTC').
        
    Возвращает:
        float: Юлианская дата.
    """
    try:
        # Локальное время с указанной временной зоной
        local_time = datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo(timezone))
        
        # Преобразование локального времени в UTC
        utc_time = local_time.astimezone(ZoneInfo('UTC'))
        
        # Вычисление Юлианской даты
        jd = (
            (utc_time - datetime(2000, 1, 1, 12, tzinfo=ZoneInfo('UTC'))).total_seconds() / 86400.0
            + 2451545.0
        )
        return jd
    
    except Exception as e:
        return f"Ошибка: {str(e)}"

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def calendar_date(julian_date, timezone='UTC'):
    """
    Преобразует Юлианскую дату (JD) в календарную дату и время с учётом временной зоны.
    
    Аргументы:
        julian_date (float): Юлианская дата.
        timezone (str, optional): Название временной зоны (например, 'Europe/Moscow', по умолчанию 'UTC').
        
    Возвращает:
        datetime: Календарная дата и время с учётом временной зоны.
    """
    try:
        # Эпоха J2000.0: Юлианская дата 2451545.0 = 1 января 2000 года, 12:00 UTC
        jd_epoch = 2451545.0
        epoch_datetime = datetime(2000, 1, 1, 12, tzinfo=ZoneInfo('UTC'))
        
        # Разница в днях между заданной JD и эпохой
        delta_days = julian_date - jd_epoch
        
        # UTC-время
        utc_datetime = epoch_datetime + timedelta(days=delta_days)
        
        # Преобразование в локальную временную зону
        local_datetime = utc_datetime.astimezone(ZoneInfo(timezone))
        
        return local_datetime
    
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Пример использования
# print(calendar_date(2460403.3533333334, timezone='Europe/Moscow'))  # Москва
# print(calendar_date(2460403.3533333334, timezone='America/New_York'))  # Нью-Йорк
# print(calendar_date(2460403.3533333334, timezone='UTC'))  # UTC


# print(julian_date(2024, 12, 8, 20, 28, 48))  
# # Результат: 2460403.3533333334
# print(julian_date(1000, 3, 1))  
# # Результат: 2086315.5
# print(julian_date(1582, 10, 4))  
# # Результат: 2299159.5 (последний день Юлианского календаря)
# print(julian_date(1582, 10, 10))  
# ValueError: Дата находится в периоде перехода между календарями (5–14 октября 1582 года).

"""
Выбор 1 января 4713 года до н. э. (по Юлианскому календарю) в качестве начальной точки отсчета для Юлианской даты связан
с несколькими практическими и историческими причинами. Это дата введена астрономом Джозефом Скалигером в 1583 году и названа
в честь его отца, Юлия Цезаря Скалигера. Вот ключевые аспекты выбора:
1. Скалигеров цикл
Джозеф Скалигер искал удобный способ выразить любую дату в одну непрерывную шкалу дней, избегая сложностей с разными календарями.
Для этого он использовал три долгосрочных календарных цикла:
Солнечный цикл (28 лет) — период, после которого календарные дни недели совпадают с днями года.
Лунный цикл Метона (19 лет) — период, после которого фазы Луны повторяются в те же календарные даты.
Индиктион (15 лет) — административный цикл, использовавшийся в Римской империи для налоговых целей.
Общий период, после которого все три цикла повторяются, равен:
28 × 19 × 15 = 7980  лет.
2. Начальная точка цикла
Скалигер определил, что 1 января 4713 года до н. э. — это момент, когда начинается 7980-летний цикл (все три цикла синхронизированы).
Выбор этой даты был удобен, поскольку:
Это время значительно раньше всех известных исторических событий и календарей (например, египетских или шумерских).
Это дает положительные числа для всех дат в исторической эпохе (т. е. нет отрицательных чисел при работе с Юлианской датой).
"""



# Пример использования
# print(julian_date(2024, 12, 8, 20, 28, 48, timezone='Europe/Moscow'))  # Москва
# print(julian_date(2024, 12, 8, 20, 28, 48, timezone='America/New_York'))  # Нью-Йорк
# print(julian_date(2024, 12, 8, 20, 28, 48, timezone='UTC'))  # UTC


# Zodiac Sign By Date

# from datetime import datetime
import random

def get_zodiac_sign(date):
    """
    Определяет знак зодиака по дате.

    :param date: объект datetime или строка в формате 'YYYY-MM-DD'.
    :return: строка с названием знака зодиака.
    """
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    zodiac_dates = [
        # Каждый элемент содержит три части: начало периода, конец периода и название знака зодиака
        ((1, 20), (2, 18), 'Водолей'),  # Водолей: с 20 января по 18 февраля
        ((2, 19), (3, 20), 'Рыбы'),     # Рыбы: с 19 февраля по 20 марта
        ((3, 21), (4, 19), 'Овен'),     # Овен: с 21 марта по 19 апреля
        ((4, 20), (5, 20), 'Телец'),    # Телец: с 20 апреля по 20 мая
        ((5, 21), (6, 20), 'Близнецы'), # Близнецы: с 21 мая по 20 июня
        ((6, 21), (7, 22), 'Рак'),      # Рак: с 21 июня по 22 июля
        ((7, 23), (8, 22), 'Лев'),      # Лев: с 23 июля по 22 августа
        ((8, 23), (9, 22), 'Дева'),     # Дева: с 23 августа по 22 сентября
        ((9, 23), (10, 22), 'Весы'),    # Весы: с 23 сентября по 22 октября
        ((10, 23), (11, 21), 'Скорпион'),# Скорпион: с 23 октября по 21 ноября
        ((11, 22), (12, 21), 'Стрелец'),# Стрелец: с 22 ноября по 21 декабря
        ((12, 22), (1, 19), 'Козерог'), # Козерог: с 22 декабря по 19 января
    ]

    for start, end, sign in zodiac_dates:
        start_date = datetime(date.year, start[0], start[1])
        end_date = datetime(date.year, end[0], end[1])

        if start_date <= date <= end_date:
            return sign

        # Для Козерога нужно учитывать переход через Новый год
        if start[0] == 12 and end[0] == 1 and (date >= start_date or date <= end_date):
            return sign

    return None

def get_random_date():
    """
    Возвращает случайную дату в формате 'YYYY-MM-DD'.
    """
    year = random.randint(1900, 2100)
    month = random.randint(1, 12)
    day = random.randint(1, 28 if month == 2 else (30 if month in [4, 6, 9, 11] else 31))
    return f"{year:04d}-{month:02d}-{day:02d}"

# Пример использования
random_date = get_random_date()
zodiac_sign = get_zodiac_sign(random_date)
print(f"Случайная дата: {random_date}, Знак зодиака: {zodiac_sign}")
