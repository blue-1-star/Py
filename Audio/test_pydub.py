from pydub import AudioSegment
import os
# Загрузка MP3 файлов

# af1 = r"G:\Music\fav\2025_winter\Josefines julesalme Trio Mediæval.mp3"
# af2 = r"G:\Music\fav\2025_winter\Josefines julesalme_repeat.mp3"
# af3 = "G:\\Music\\fav\\2025_winter\\Josefines julesalme Trio Mediæval.mp3"
# af4 = "G:\\Music\\fav\\2025_winter\\Josefines julesalme_repeat.mp3"

# af_comb = r"G:\Music\fav\2025_winter\Josefines julesalme.mp3"
# # a1 = AudioSegment.from_file(af3)
# # a2 = AudioSegment.from_file(af4)
# a1 = AudioSegment.from_file("G:\\Music\\fav\\2025_winter\\Josefines julesalme Trio Mediæval.mp3")
# a2 = AudioSegment.from_file("G:\\Music\\fav\\2025_winter\\Josefines julesalme_repeat.mp3")
# # Склеивание
# af_comb = a1 + a2

# # Сохранение результата
# combined.export(af_comb, format="mp3")
# "G:\Music\fav\2025_winter\Josefines julesalme_repeat.mp3"

# from pydub import AudioSegment

# Путь к файлам
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
audio_dir = r"G:\Music\fav\2025_winter"

# af1 = r"G:\Music\fav\2025_winter\Josefines julesalme Trio Mediæval.mp3"

# af2 = r"G:\Music\fav\2025_winter\Josefines julesalme_repeat.mp3"
# af_comb = r"G:\Music\fav\2025_winter\Josefines_combined.mp3"
a1 = os.path.join(audio_dir, "Josefines julesalme Trio Mediæval.mp3")
a2 = os.path.join(audio_dir, "Josefines julesalme_repeat.mp3")
af_comb = os.path.join(audio_dir, "Josefines_combined.mp3")
if os.path.exists(a1):
    print(f"file {a1}: exists")
if os.path.exists(a2):
    print(f"file {a2}: exists")    
# try:
    # Загрузка MP3 файлов
as1 = AudioSegment.from_file(a1)
as2 = AudioSegment.from_file(a2)

    # Склеивание
combined = a1 + a2

    # Сохранение результата
combined.export(af_comb, format="mp3")
# print("Файл успешно создан:", af_comb)

# except FileNotFoundError as e:
    # print("Файл не найден:", e)
# except Exception as e:
    # print("Ошибка:", e)
