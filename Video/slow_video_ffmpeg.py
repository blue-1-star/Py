def slow_down_audio_ffmpeg(input_path, output_path, speed_factor=0.5):
    # Проверка диапазона atempo (0.5 - 2.0)
    if speed_factor < 0.5 or speed_factor > 2.0:
        audio_filter = f"atempo={min(speed_factor, 2.0)},atempo={max(speed_factor / 2, 0.5)}"
    else:
        audio_filter = f"atempo={speed_factor}"
    
    # ffmpeg команда для аудио
    command = [
        'ffmpeg',
        '-i', input_path,         # Входной файл
        '-af', audio_filter,      # Аудиофильтр для изменения скорости
        '-c:a', 'libmp3lame',     # MP3 кодек
        '-b:a', '320k',           # Высокое качество MP3 (320 kbps)
        output_path               # Выходной файл
    ]
def slow_down_video_ffmpeg(input_path, output_path, speed_factor=0.5):
    video_speed = 1 / speed_factor
    
    if speed_factor < 0.5 or speed_factor > 2.0:
        audio_filter = f"atempo={min(speed_factor, 2.0)},atempo={max(speed_factor / 2, 0.5)}"
    else:
        audio_filter = f"atempo={speed_factor}"
    
    # ffmpeg команда для видео и аудио
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f"setpts={video_speed}*PTS",
        '-af', audio_filter,
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',        # Только для видео
        '-c:a', 'aac',
        '-b:a', '192k',
        output_path
    ]
    
    subprocess.run(command, check=True)

# Пример
slow_down_video_ffmpeg('input_video.mp4', 'output_slow.mp4', speed_factor=0.7)
  
    # Выполнение команды
subprocess.run(command, check=True)

# Пример использования
# slow_down_audio_ffmpeg('input_audio.mp3', 'output_slow.mp3', speed_factor=0.7)


# Пример использования
inp_video = r"G:\My\sov\tmp\sov_tea.mp4"
output_slow = r"G:\My\sov\tmp\sov_tea_s.mp3"
slow_down_video_ffmpeg(inp_video, output_slow, speed_factor=0.7)

