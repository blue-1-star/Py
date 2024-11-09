import subprocess
from datetime import datetime
import pytz

def get_video_creation_date(video_path):
    try:
        # Запуск exiftool для получения даты создания
        result = subprocess.run(
            ['G:/Soft/PORTABLE/exiftool', '-CreateDate', '-d', '%Y-%m-%d %H:%M:%S', video_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output:
            # Извлечение строки даты из вывода
            creation_date_str = output.split(':', 1)[1].strip()
            # Парсинг даты
            creation_date = datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
            # Установка временной зоны UTC
            creation_date_utc = pytz.utc.localize(creation_date)
            return creation_date_utc
        else:
            return "Дата создания не найдена"
    except Exception as e:
        return str(e)

# Путь к видеофайлам
video_path1 = 'g:/test/VID_20230527_133445.mp4'
video_path2 = 'g:/test/VID_20240528_160201.mp4'
video_path3 = 'G:/Photo/OnePlus/Video/VID_20220719_115940.mp4'

# Получение даты создания файлов
dates = [get_video_creation_date(video_path) for video_path in [video_path1, video_path2, video_path3]]

# Часовой пояс устройства (например, Europe/Kiev)
device_timezone = pytz.timezone('Europe/Kiev')  # Укажите ваш часовой пояс

# Конвертация времени из UTC в местное время устройства
converted_dates = [
    date.astimezone(device_timezone) if isinstance(date, datetime) else date
    for date in dates
]

print(f'Оригинальные даты создания видеофайлов (UTC): {dates}')
print(f'Конвертированные даты создания видеофайлов (местное время): {converted_dates}')
