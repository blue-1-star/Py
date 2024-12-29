from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
# from moviepy.video.fx.all import speedx
from moviepy.video.fx.speedx import speedx

import os

def slow_down_video(input_path, output_path, speed_factor=0.5):
    video = VideoFileClip(input_path)
    
    # Применяем замедление к видео
    slowed_video = video.fx(speedx, speed_factor)
    
    # Применяем замедление к аудио
    slowed_audio = video.audio.fx(speedx, speed_factor)
    
    # Назначаем новое аудио к видео
    final_video = slowed_video.set_audio(slowed_audio)
    
    # Сохраняем результат
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    # Закрываем клипы
    video.close()
    slowed_video.close()
    slowed_audio.close()

# Пример использования
inp_video = r"G:\My\sov\tmp\sov_tea.mp4"
output_slow = r"G:\My\sov\tmp\sov_tea_s.mp3"
slow_down_video(inp_video, output_slow, speed_factor=0.7)
