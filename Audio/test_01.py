import os
from pydub import AudioSegment
from pydub.utils import which

# Настройка FFmpeg
# AudioSegment.converter = which("ffmpeg")  # Убедитесь, что FFmpeg доступен
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"
audio_dir = r"G:\Music\fav\2025_winter"

a1 = os.path.join(audio_dir, "Josefines julesalme Trio Mediæval.mp3")
a2 = os.path.join(audio_dir, "Josefines julesalme_repeat.mp3")
af_comb = os.path.join(audio_dir, "Josefines_combined.mp3")

# Проверка существования файлов
if os.path.exists(a1) and os.path.exists(a2):
    print(f"Файлы существуют: \n{a1}\n{a2}")
else:
    print("Один из файлов не найден")
    exit()

# Загрузка и склеивание
try:
    as1 = AudioSegment.from_file(a1)
    as2 = AudioSegment.from_file(a2)
    combined = as1 + as2
    combined.export(af_comb, format="mp3")
    print(f"Склеенный файл сохранён: {af_comb}")
except Exception as e:
    print("Ошибка при обработке аудио:", e)
