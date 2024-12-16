# from skyfield.api import load

# def get_last_new_moon():
#     eph = load('de421.bsp')
#     ts = load.timescale()
#     e, m = eph['earth'], eph['moon']

#     # Ищем время, когда Луна пересекает Солнце (новолуние)
#     t0 = ts.now().utc_jpl()  # Текущее время
#     t1 = ts.utc(t0.utc.year, t0.utc.month, t0.utc.day + 1)
#     f = eph['sun'].observe_from(e).apparent()
#     t, _ = ts.find_maxima(lambda t: -f.separation_from(eph['moon'].observe_from(e)).degrees)
#     return t.utc_iso()

# new_moon_time = get_last_new_moon()
# print(new_moon_time)
# 
# 
from skyfield.api import load
from skyfield.almanac import find_discrete, moon_phases

def get_last_new_moon():
    # Загружаем эфемериды
    eph = load('de421.bsp')  # Эфемериды JPL DE421
    ts = load.timescale()

    # Текущее время
    t0 = ts.now()
    t1 = ts.utc(t0.utc_datetime().year, t0.utc_datetime().month, t0.utc_datetime().day + 1)

    # Получаем фазы Луны и ищем новолуние
    f = moon_phases(eph)
    times, phases = find_discrete(t0 - 30, t1, f)  # Интервал поиска: 30 дней до текущего момента

    # Находим последнее новолуние (фаза = 0)
    for t, phase in zip(times, phases):
        if phase == 0:
            return t

# Используем функцию
new_moon_time = get_last_new_moon()
print(f"Последнее новолуние: {new_moon_time.utc_iso()}")

from astropy.time import Time
from astropy.coordinates import get_sun, get_body, solar_system_ephemeris
import numpy as np
import astropy.units as u

def get_last_new_moon_astro():
    """
    Находит последнее новолуние относительно текущего момента с использованием Astropy.
    """
    # Текущее время
    t_now = Time.now()

    # Начнем поиск за 30 дней до текущего момента
    t_start = t_now - 30 * u.day
    t_end = t_now
    dt = 0.01  # Шаг по времени в днях

    # Генерируем массив временных моментов для поиска
    times = t_start + np.arange(0, (t_end - t_start).value, dt) * u.day

    # Используем точные эфемериды для вычислений
    with solar_system_ephemeris.set('builtin'):
        sun_coords = get_sun(times)  # Координаты Солнца
        moon_coords = get_body("moon", times)  # Координаты Луны

    # Вычисляем угловое расстояние между Солнцем и Луной
    phase_angles = sun_coords.separation(moon_coords)

    # Находим минимальное угловое расстояние (момент новолуния)
    new_moon_index = np.argmin(phase_angles)

    # Возвращаем время последнего новолуния
    last_new_moon_time = times[new_moon_index]

    return last_new_moon_time

# Используем функцию
new_moon_time = get_last_new_moon_astro()
print(f"Последнее новолуние_astropy: {new_moon_time.iso}")
