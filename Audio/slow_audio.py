from moviepy import *  # Импорт всех доступных функций
from moviepy.audio.io.AudioFileClip import AudioFileClip  # Явный импорт AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

# def slow_down_audio(video_path, output_path, speed_factor=0.5):
#     """
#     Уменьшает скорость воспроизведения аудио в видео.
    
#     :param video_path: Путь к исходному видеофайлу
#     :param output_path: Путь для сохранения нового видеофайла
#     :param speed_factor: Коэффициент замедления (меньше 1 для замедления)
#     """
#     # Загрузка видео
#     video = VideoFileClip(video_path)
    
#     # Замедление аудио
#     audio = video.audio
#     if audio:
#         slowed_audio = audio.fx(vfx.speedx, speed_factor)
        
#         # Установка нового аудио на видео
#         video = video.set_audio(slowed_audio)
    
#     # Сохранение видео
#     video.write_videofile(output_path, codec='libx264', audio_codec='aac')

#
#
#
from moviepy.audio.io.AudioFileClip import AudioFileClip

def slow_down_audio(input_path, output_path, speed_factor=0.5):
    audio = AudioFileClip(input_path)
    
    # Меняем частоту кадров для замедления
    # slowed_audio = audio.set_duration(audio.duration / speed_factor)
    slowed_audio = audio.with_duration(audio.duration / speed_factor)
    # Сохраняем результат
    slowed_audio.write_audiofile(output_path)
    slowed_audio.close()



# Пример использования:
inp_video = r"G:\My\sov\tmp\sov_tea.mp4"
output_video = r"G:\My\sov\tmp\sov_tea_s.mp3"
slow_down_audio(inp_video, output_video, speed_factor=0.7)
# slow_down_audio('input.mp3', 'output_slow.mp3', speed_factor=0.5)
