from pytube import YouTube
from moviepy import *
from moviepy import *  # Импорт всех доступных функций
from moviepy.audio.io.AudioFileClip import AudioFileClip  # Явный импорт AudioFileClip

import os


def download_and_convert_to_mp3(url, output_directory='.'):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        if not video:
            print("Аудио поток не найден.")
            return
        
        print(f"Скачиваем: {yt.title}...")
        downloaded_file = video.download(output_path=output_directory)
        
        base, ext = os.path.splitext(downloaded_file)
        mp3_file = f"{base}.mp3"
        
        print("Конвертация в mp3...")
        audio_clip = AudioFileClip(downloaded_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()
        
        os.remove(downloaded_file)
        
        print(f"Готово! Файл сохранен как: {mp3_file}")
    
    except Exception as e:
        print(f"Ошибка: {e}")

# Пример использования
# download_and_convert_to_mp3('https://www.youtube.com/watch?v=dQw4w9WgXcQ', output_directory='./music')
output_directory = r"G:\Music\fav\2025_winter"
download_and_convert_to_mp3('https://music.youtube.com/watch?v=1W6MYRTMvpA', output_directory)
