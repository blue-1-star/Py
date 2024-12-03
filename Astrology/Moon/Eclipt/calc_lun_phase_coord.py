import math
import os
from datetime import datetime
from FileSys.lib_files import get_full_file_path
# Константы для вычислений
SYNODIC_MONTH = 29.53058867  # Средняя продолжительность лунного месяца в днях
OBLIQUITY = 23.44  # Наклон эклиптики (в градусах)
ECCENTRICITY = 0.0549  # Эксцентриситет орбиты Луны

# Средние элементы орбиты Луны (градусы)
MEAN_LONGITUDE_MOON = 218.316  # Средняя долгота Луны
MEAN_ELONGATION = 297.850  # Среднее удаление Луны от Солнца
MEAN_ANOMALY = 134.963  # Средняя аномалия Луны
MEAN_DISTANCE = 93.272  # Среднее расстояние Луны от восходящего узла орбиты

# Коэффициенты для поправок эклиптической долготы
COEFF_LONGITUDE = {
    "mean_anomaly": 6.289,  # Угловая поправка из средней аномалии
    "elongation_anomaly": -1.274,  # Поправка из разности аномалий и удаления
    "elongation": 0.658,  # Поправка из удвоенного удаления
    "double_mean_anomaly": -0.214,  # Поправка из удвоенной средней аномалии
    "single_elongation": -0.11,  # Поправка из удаления
}

# Коэффициент для вычисления эклиптической широты
COEFF_LATITUDE = 5.128  # Поправка на эклиптическую широту

# Радиус орбиты Луны в километрах
MOON_ORBIT_RADIUS = 385000

# Начальное значение известного новолуния
KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)

def normalize_angle(angle):
    """Нормализует угол в диапазон [0, 360)"""
    return angle % 360

def calculate_lunar_phase_and_coordinates(current_time):
    """Вычисляет фазу Луны, эклиптические координаты и расстояние до Луны."""
    # Фиксация времени расчёта
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # День синодического месяца
    days_since_known_new_moon = (current_time - KNOWN_NEW_MOON).total_seconds() / (24 * 3600)
    lunar_day = days_since_known_new_moon % SYNODIC_MONTH
    phase = (lunar_day / SYNODIC_MONTH) * 100  # Процент фазы

    # Средние элементы орбиты
    mean_longitude = MEAN_LONGITUDE_MOON + 13.176396 * days_since_known_new_moon
    elongation = MEAN_ELONGATION + 13.176396 * days_since_known_new_moon
    mean_anomaly = MEAN_ANOMALY + 13.176396 * days_since_known_new_moon
    mean_distance = MEAN_DISTANCE + 13.176396 * days_since_known_new_moon

    # Нормализация углов
    mean_longitude = normalize_angle(mean_longitude)
    elongation = normalize_angle(elongation)
    mean_anomaly = normalize_angle(mean_anomaly)
    mean_distance = normalize_angle(mean_distance)

    # Эклиптическая долгота
    longitude = mean_longitude
    longitude += COEFF_LONGITUDE["mean_anomaly"] * math.sin(math.radians(mean_anomaly))
    longitude += COEFF_LONGITUDE["elongation_anomaly"] * math.sin(math.radians(2 * elongation - mean_anomaly))
    longitude += COEFF_LONGITUDE["elongation"] * math.sin(math.radians(2 * elongation))
    longitude += COEFF_LONGITUDE["double_mean_anomaly"] * math.sin(math.radians(2 * mean_anomaly))
    longitude += COEFF_LONGITUDE["single_elongation"] * math.sin(math.radians(elongation))
    longitude = normalize_angle(longitude)

    # Эклиптическая широта
    latitude = COEFF_LATITUDE * math.sin(math.radians(mean_distance))

    # Расстояние до Луны
    distance = MOON_ORBIT_RADIUS * (1 - ECCENTRICITY**2) / (1 + ECCENTRICITY * math.cos(math.radians(mean_anomaly)))

    return {
        "timestamp": timestamp,
        "phase": phase,
        "lunar_day": lunar_day,
        "longitude": longitude,
        "latitude": latitude,
        "distance": distance,
    }

# def get_full_file_path(filename):
#     """
#     Возвращает полный путь к файлу данных, находящемуся в той же директории,
#     что и текущий скрипт, или в указанной поддиректории.
#     """
#     script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
#     return os.path.join(script_dir, filename)
def save_results_to_file(data, filename="lunar_data.txt"):
    """Сохраняет результаты вычислений в файл."""

    # file_path = "G:\\Programming\\Py\\Astrology\\Moon\\Eclipt\\"+filename
    # script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
    # file_path = os.path.join(script_dir, filename)
    file_path = get_full_file_path(filename)
    
    # file_p_getcwd= os.getcwd()+filename
    # print(f"getcwd(): {os.getcwd()}")
    # print(f"dirname:  {os.path.dirname(os.path.abspath(__file__))}")
    # print(f"full_path:  {os.path.join(script_dir, filename)}")
    
    with open(file_path, "a") as file:
        file.write(f"Время расчёта: {data['timestamp']}\n")
        file.write(f"Фаза Луны: {data['phase']:.2f}%\n")
        file.write(f"Лунный день: {data['lunar_day']:.2f}\n")
        file.write(f"Эклиптическая долгота: {data['longitude']:.6f}°\n")
        file.write(f"Эклиптическая широта: {data['latitude']:.6f}°\n")
        file.write(f"Расстояние до Луны: {data['distance']:.2f} км\n")
        file.write("-" * 40 + "\n")


# Пример использования
current_time = datetime.utcnow()
results = calculate_lunar_phase_and_coordinates(current_time)
save_results_to_file(results)

print(f"Результаты сохранены в файл. Фаза Луны: {results['phase']:.2f}%, Расстояние: {results['distance']:.2f} км.")

import csv
import re

def parse_lunar_txt_to_csv(input_file="lunar_data.txt", output_file="test_data.csv"):
    """Преобразует текстовый файл с данными Луны в CSV."""
    inp_file_path = get_full_file_path(input_file)
    out_file_path = get_full_file_path(output_file)
    data = []
    with open(inp_file_path, "r") as file:
        lines = file.readlines()
    
    # Парсинг данных из файла
    record = {}
    for line in lines:
        if line.startswith("Время расчёта:"):
            record["timestamp"] = line.split(": ")[1].strip()
        elif line.startswith("Фаза Луны:"):
            record["phase"] = float(line.split(": ")[1].replace("%", "").strip())
        elif line.startswith("Лунный день:"):
            record["day"] = float(line.split(": ")[1].strip())
        elif line.startswith("Эклиптическая долгота:"):
            record["longitude"] = float(line.split(": ")[1].replace("°", "").strip())
        elif line.startswith("Эклиптическая широта:"):
            record["latitude"] = float(line.split(": ")[1].replace("°", "").strip())
        elif line.startswith("Расстояние до Луны:"):
            record["distance"] = float(line.split(": ")[1].replace("км", "").strip())
        elif line.strip() == "----------------------------------------":
            if record:  # Сохраняем запись, если она заполнена
                data.append(record)
                record = {}

    # Запись данных в CSV
    with open(out_file_path, "w", newline="") as csvfile:
        fieldnames = ["timestamp", "phase", "longitude", "latitude", "distance", "day"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Данные успешно сохранены в файл {output_file}.")

# Пример использования
parse_lunar_txt_to_csv()
