import subprocess
from datetime import datetime, timedelta
import pytz

def get_video_creation_date(video_path):
    try:
        result = subprocess.run(
            ['G:/Soft/PORTABLE/exiftool', '-CreateDate', '-d', '%Y-%m-%d %H:%M:%S', video_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output:
            creation_date_str = output.split(':', 1)[1].strip()
            creation_date = datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
            return creation_date
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

# Часовой пояс устройства (например, UTC+3)
device_timezone = pytz.timezone('Europe/Kiev')  # Укажите ваш часовой пояс

# Конвертация времени из метаданных в местное время устройства
converted_dates = [date.astimezone(device_timezone) if isinstance(date, datetime) else date for date in dates]

print(f'Оригинальные даты создания видеофайлов: {dates}')
print(f'Конвертированные даты создания видеофайлов: {converted_dates}')
