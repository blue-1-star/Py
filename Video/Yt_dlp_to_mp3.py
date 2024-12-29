import yt_dlp

def download_and_convert_to_mp3(url, output_directory='.'):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{output_directory}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Файл успешно загружен и конвертирован в mp3.")
    
    except Exception as e:
        print(f"Ошибка: {e}")

output_directory = r"G:\Music\fav\2025_winter"
download_and_convert_to_mp3('https://music.youtube.com/watch?v=1W6MYRTMvpA', output_directory)
