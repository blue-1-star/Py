import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import re

def sanitize_filename(name):
    # Удаление недопустимых символов для имени файла
    return re.sub(r'[\\/*?:"<>|]', "", name)
def download_and_convert_to_mp3(url, output_directory='.'):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{output_directory}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '360',
            }],
            'postprocessor_args': ['-metadata', 'title=%(title)s', '-metadata', 'artist=%(uploader)s'],
            'noplaylist': True  # 👈 Важно: не загружать весь плейлист
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # title = info_dict.get('title', 'Unknown Title')
            title = sanitize_filename(info_dict.get('title', 'Unknown Title'))
            artist = info_dict.get('uploader', 'Unknown Artist')
            album = info_dict.get('album', 'YouTube')
            # year = info_dict.get('year', 'YouTube')
            year = info_dict.get('release_date', '2024').split('-')[0]  # Берём только год
            # Получаем путь к mp3 файлу
            mp3_path = os.path.join(output_directory, f"{title}.mp3")
            
            # Добавляем метаданные
            audio = EasyID3(mp3_path)
            audio['title'] = title
            audio['artist'] = artist
            audio['album'] = album
            audio['date'] = year
            audio.save()

            print(f"Файл успешно загружен и конвертирован в mp3: {mp3_path}")
    
    except Exception as e:
        print(f"Ошибка: {e}")

# Пример использования
output_directory = r"G:\Music\fav\2025_spring"
web_source = "https://www.youtube.com/watch?v=PgXd_93og6o&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&index=27"
# download_and_convert_to_mp3('https://www.youtube.com/watch?v=07lcIkYEK-g', output_directory)
download_and_convert_to_mp3(web_source, output_directory)

