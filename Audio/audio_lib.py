from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
def trim_audio(input_path, output_path, start_ms, end_ms):
    """
    Обрезает аудиофайл и сохраняет результат.

    :param input_path: str, путь к исходному аудиофайлу
    :param output_path: str, путь для сохранения обрезанного аудиофайла
    :param start_ms: int, начальная точка обрезки в миллисекундах
    :param end_ms: int, конечная точка обрезки в миллисекундах
    """
    try:
        # Загрузка аудиофайла
        audio = AudioSegment.from_file(input_path)

        # Проверка границ обрезки
        if start_ms < 0 or end_ms > len(audio):
            raise ValueError("Границы обрезки выходят за пределы длины аудиофайла.")

        if start_ms >= end_ms:
            raise ValueError("Начальная точка обрезки должна быть меньше конечной.")

        # Обрезка аудио
        trimmed_audio = audio[start_ms:end_ms]

        # Сохранение обрезанного файла
        trimmed_audio.export(output_path, format="mp3")
        print(f"Обрезанный файл сохранён: {output_path}")

    except Exception as e:
        print(f"Ошибка: {e}")


def concatenate_audio(file1, file2, output_file):
    # Загружаем первый аудиофайл
    audio1 = AudioSegment.from_file(file1)
    
    # Загружаем второй аудиофайл
    audio2 = AudioSegment.from_file(file2)
    
    # Склеиваем аудиофайлы
    combined = audio1 + audio2
    

    # Экспортируем результат в новый файл
    combined.export(output_file, format="mp3")
    print(f"Аудиофайлы склеены и сохранены в {output_file}")
    # Копируем метаданные из первого файла в результирующий файл
    copy_metadata(file1, output_file)
def copy_metadata(source_file, target_file):
    # Загружаем метаданные из исходного файла
    source_audio = MP3(source_file, ID3=ID3)
    target_audio = MP3(target_file, ID3=ID3)
    
    # Копируем теги
    if source_audio.tags:
        for tag in source_audio.tags.keys():
            target_audio.tags[tag] = source_audio.tags[tag]
    
    # Сохраняем метаданные в результирующий файл
    target_audio.save()

# Пример использования


# Пример использования
if __name__ == "__main__":
    # input_file1 = r"G:\Music\fav\2025_winter\Не люби меня CHEPIKK Премьера 2025 (Ochamchira Music) 0.mp3"
    input_file1 = r"G:\Music\fav\2025_winter\Ochamchira_Не люби меня.mp3"
    input_file2 = r"G:\Music\fav\2025_winter\Ochamchira не люби меня.mp3"
    # input_file1 = r"G:\Music\fav\2025_winter\Не люби меня CHEPIKK Премьера 2025 (Ochamchira Music) 0.mp3"
    output_file = r"G:\Music\fav\2025_winter\Ochamchira_Не люби меня_5.mp3"

    concatenate_audio( input_file1, input_file2, output_file)
    # start_time = 10000  # Начало обрезки в миллисекундах (10 секунд)
    # end_time = 30000    # Конец обрезки в миллисекундах (30 секунд)

    # trim_audio(input_file, output_file, start_time, end_time)
