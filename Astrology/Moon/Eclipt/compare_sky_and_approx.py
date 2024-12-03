import os
from datetime import datetime
from math import degrees
from skyfield.api import load
import math
import csv


# --- Приближённые расчёты ---
def approx_moon(date=None):
    if date is None:
        date = datetime.now()
    julian_date = (date - datetime(2000, 1, 1)).days + 2451545.0

    MEAN_LONGITUDE_MOON = 218.316
    MEAN_ELONGATION = 297.850
    MEAN_ANOMALY = 134.963
    MEAN_DISTANCE = 93.272

    days_since_epoch = julian_date - 2451545.0
    mean_longitude = MEAN_LONGITUDE_MOON + 13.176396 * days_since_epoch
    mean_anomaly = MEAN_ANOMALY + 13.064993 * days_since_epoch
    elongation = MEAN_ELONGATION + 13.176396 * days_since_epoch

    longitude = mean_longitude + 6.289 * math.sin(math.radians(mean_anomaly))
    latitude = 5.128 * math.sin(math.radians(MEAN_DISTANCE))
    distance = 385000 * (1 - 0.0549**2) / (1 + 0.0549 * math.cos(math.radians(mean_anomaly)))

    longitude %= 360
    latitude %= 360

    moon_phase = (1 - math.cos(math.radians(elongation))) / 2
    lunar_day = (elongation % 360) / 12.2

    return {
        "longitude": longitude,
        "latitude": latitude,
        "distance_km": distance,
        "moon_phase": moon_phase,
        "lunar_day": lunar_day
    }


# --- Точные вычисления Skyfield ---
def skyfield_moon(date=None):
    if date is None:
        date = datetime.now()

    ts = load.timescale()
    t = ts.utc(date.year, date.month, date.day, date.hour, date.minute, date.second)

    eph = load('de421.bsp')
    earth = eph['earth']
    moon = eph['moon']

    astrometric = earth.at(t).observe(moon).apparent()
    ecliptic = astrometric.ecliptic_latlon()

    sun = eph['sun']
    # elongation = degrees(earth.at(t).observe(moon).apparent().separation_from(earth.at(t).observe(sun).apparent()))
    elongation = earth.at(t).observe(moon).apparent().separation_from(earth.at(t).observe(sun).apparent()).degrees

    moon_phase = (1 - math.cos(math.radians(elongation))) / 2
    lunar_day = (elongation % 360) / 12.2

    return {
        "longitude": ecliptic[1].degrees,
        "latitude": ecliptic[0].degrees,
        "distance_km": astrometric.distance().km,
        "moon_phase": moon_phase,
        "lunar_day": lunar_day
    }


# --- Извлечение дат из файла ---
def extract_timestamps(file_path):
    if not os.path.exists(file_path):
        return []

    dates = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Время расчёта:"):
                try:
                    timestamp = line.split(": ", 1)[1].strip()
                    date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    dates.append(date)
                except ValueError:
                    continue  # Пропускаем строки с некорректным форматом времени
    return dates


# --- Формирование таблицы сравнений ---
def compare_results(dates):
    with open('comparison_results.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'Date',
            'Approx Longitude', 'Skyfield Longitude',
            'Approx Latitude', 'Skyfield Latitude',
            'Approx Distance (km)', 'Skyfield Distance (km)',
            'Approx Moon Phase', 'Skyfield Moon Phase',
            'Approx Lunar Day', 'Skyfield Lunar Day'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for date in dates:
            approx = approx_moon(date)
            skyfield = skyfield_moon(date)

            writer.writerow({
                'Date': date,
                'Approx Longitude': approx['longitude'],
                'Skyfield Longitude': skyfield['longitude'],
                'Approx Latitude': approx['latitude'],
                'Skyfield Latitude': skyfield['latitude'],
                'Approx Distance (km)': approx['distance_km'],
                'Skyfield Distance (km)': skyfield['distance_km'],
                'Approx Moon Phase': approx['moon_phase'],
                'Skyfield Moon Phase': skyfield['moon_phase'],
                'Approx Lunar Day': approx['lunar_day'],
                'Skyfield Lunar Day': skyfield['lunar_day']
            })


# --- Основная логика ---
file_path = 'lunar_data.txt'
dates = extract_timestamps(file_path)

if not dates:
    dates = [datetime.now()]

compare_results(dates)
print("Таблица сравнений сохранена в 'comparison_results.csv'.")
