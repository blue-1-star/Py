from datetime import datetime

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

# Пример использования:
date = datetime(1952, 7, 30)  # Задайте нужную дату
phase, phase_name = moon_phase(date)
print(f"Фаза Луны: {phase} (около {phase_name})")
