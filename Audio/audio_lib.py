from pydub import AudioSegment

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

# Пример использования
if __name__ == "__main__":
    input_file = r"G:\Music\fav\2025_winter\Josefines julesalme Trio Mediæval.mp3"
    output_file = r"G:\Music\fav\2025_winter\Josefines_trimmed.mp3"
    start_time = 10000  # Начало обрезки в миллисекундах (10 секунд)
    end_time = 30000    # Конец обрезки в миллисекундах (30 секунд)

    trim_audio(input_file, output_file, start_time, end_time)
