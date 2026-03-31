import subprocess
import os
import sys

def download_youtube_clip(url, start_time, end_time, output_filename):
    """
    Скачивает и вырезает фрагмент из YouTube видео.
    
    Параметры:
    url (str): ссылка на YouTube видео
    start_time (str): время начала в формате "ММ:СС" или "ЧЧ:ММ:СС"
    end_time (str): время конца в том же формате
    output_filename (str): имя выходного файла (без расширения)
    """
    # https://www.youtube.com/watch?v=TJOXolrZ6pI
    #  01:01:10.   01:04:11
    
    # Автоматически добавляем расширение .mp3, если его нет
    if not output_filename.endswith('.mp3'):
        output_filename += '.mp3'
    
    # Формируем команду yt-dlp
    command = [
        'yt-dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--postprocessor-args', f'-ss {start_time} -to {end_time}',
        '-o', output_filename,
        url
    ]
    
    print(f"🎵 Скачиваю и вырезаю фрагмент {start_time} - {end_time}...")
    print(f"💾 Сохраняю как: {output_filename}")
    print("-" * 50)
    
    try:
        # Запускаем процесс и выводим результат в реальном времени
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Выводим прогресс построчно
        for line in process.stdout:
            print(line, end='')
            
        process.wait()
        
        if process.returncode == 0:
            print("\n✅ Готово! Файл сохранён.")
        else:
            print(f"\n❌ Ошибка при выполнении (код: {process.returncode})")
            
    except FileNotFoundError:
        print("❌ yt-dlp не найден! Убедитесь, что он установлен.")
        print("   Установить можно командой: brew install yt-dlp")
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")

def main():
    """Основная функция с простым интерфейсом"""
    
    print("🎬 Скачиватель треков с YouTube")
    print("=" * 50)
    
    # Просим пользователя ввести данные
    url = input("📎 Вставьте ссылку на YouTube: ").strip()
    
    start = input("⏱️ Время начала (например 12:34 или 01:23:45): ").strip()
    
    end = input("⏱️ Время конца (например 15:45 или 01:26:45): ").strip()
    
    default_name = "my_track"
    name = input(f"💾 Имя файла (Enter для '{default_name}'): ").strip()
    
    if not name:
        name = default_name
    
    print()
    
    # Вызываем функцию скачивания
    download_youtube_clip(url, start, end, name)

# Точка входа
if __name__ == "__main__":
    main()