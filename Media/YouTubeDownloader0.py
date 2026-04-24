#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Импортируем наш класс путей
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import paths


# ========== ВСЕ ПУТИ БЕРУТСЯ ИЗ paths ==========
BASE_MUSIC_DIR = paths.BASE_MUSIC_DIR
TMP_DIR = paths.TMP_DIR
LOG_DIR = paths.LOG_DIR


class YouTubeDownloader:
    """Класс для скачивания треков с YouTube"""
    
    def __init__(self):
        """Инициализация загрузчика"""
        # Создаём все необходимые папки
        self.season_dir = paths.ensure_directories()
        self.tmp_dir = TMP_DIR
        self.log_dir = LOG_DIR
        
        # Файл лога
        self.log_file = paths.get_log_file()
        
        print(f"📁 Сезонная папка: {self.season_dir}")
        print(f"📁 Временная папка: {self.tmp_dir}")
        print(f"📁 Папка логов: {self.log_dir}")
    
    def log(self, message):
        """Записывает сообщение в лог"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except:
            pass
    
    def get_video_info(self, url, timeout=60):
        """
        Получает информацию о видео: название, длительность.
        timeout: максимальное время ожидания в секундах.
        """
        try:
            # Получаем название с таймаутом
            title_result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--get-title', url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            original_title = title_result.stdout.strip() if title_result.returncode == 0 else None
            
            # Получаем длительность с таймаутом
            duration_result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--get-duration', url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            duration = duration_result.stdout.strip() if duration_result.returncode == 0 else None
            
            return original_title, duration
            
        except subprocess.TimeoutExpired:
            self.log(f"Ошибка: превышен таймаут ({timeout} сек) при получении информации для {url}")
            return None, None
        except Exception as e:
            self.log(f"Ошибка получения информации: {e}")
            return None, None        

    def parse_duration_to_seconds(self, duration_str):
        """Преобразует длительность в секунды"""
        parts = duration_str.split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(parts[0])
    
    def is_long_clip(self, duration_str, threshold_minutes=10):
        """Определяет, является ли видео длинным клипом"""
        if not duration_str:
            return False
        seconds = self.parse_duration_to_seconds(duration_str)
        return seconds > threshold_minutes * 60
    
    def clean_filename1(self, title):
        """Очищает название файла от недопустимых символов"""
        clean = re.sub(r'[<>:"/\\|?*]', '', title)
        clean = re.sub(r'\s+', '_', clean)
        clean = clean[:100]
        return clean
    def clean_filename(self, title):
        """Очищает название файла от недопустимых символов, сохраняя пробелы"""
        # Удаляем запрещённые символы для имен файлов
        clean = re.sub(r'[<>:"/\\|?*]', '', title)
        # Оставляем пробелы как есть (НЕ заменяем на подчёркивания)
        # Убираем только множественные пробелы
        clean = re.sub(r'\s+', ' ', clean)
        # Убираем пробелы в начале и конце
        clean = clean.strip()
        # Ограничиваем длину
        clean = clean[:100]
        return clean
    
    def get_next_filename(self, base_name, target_dir):
        """Получает следующее доступное имя файла"""
        counter = 1
        while True:
            if counter == 1:
                filename = f"{base_name}.mp3"
            else:
                filename = f"{base_name}_{counter}.mp3"
            
            full_path = target_dir / filename
            if not full_path.exists():
                return full_path, filename
            counter += 1
    
    def download_full(self, url, target_dir, filename=None):
        """Скачивает полное видео/аудио целиком"""
        if not filename:
            title, _ = self.get_video_info(url)
            if title:
                base_name = self.clean_filename(title)
            else:
                base_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            base_name = filename
        
        full_path, final_name = self.get_next_filename(base_name, target_dir)
        
        self.log(f"Скачивание полного файла: {final_name}")
        
        command = [
            'yt-dlp',
            '--remote-components', 'ejs:github',  # ← ДОБАВИТЬ
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', str(full_path),
            url
        ]
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )
            
            for line in process.stdout:
                if any(key in line for key in ['%', 'Destination', 'ERROR']):
                    print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"✅ Скачано: {final_name}")
                return full_path
            else:
                self.log(f"❌ Ошибка скачивания")
                return None
                
        except Exception as e:
            self.log(f"Ошибка: {e}")
            return None
    
    def download_clip(self, url, start_time, end_time, target_dir, filename=None):
        """Скачивает и вырезает фрагмент"""
        if not filename:
            title, _ = self.get_video_info(url)
            if title:
                base_name = self.clean_filename(title)
            else:
                base_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            base_name = filename
        
        full_path, final_name = self.get_next_filename(base_name, target_dir)
        
        self.log(f"Вырезание фрагмента {start_time} - {end_time} -> {final_name}")
        
        command = [
            'yt-dlp',
            '--remote-components', 'ejs:github',  # ← ДОБАВИТЬ
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--postprocessor-args', f'-ss {start_time} -to {end_time}',
            '-o', str(full_path),
            url
        ]
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )
            
            for line in process.stdout:
                if any(key in line for key in ['%', 'Destination', 'ERROR']):
                    print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"✅ Сохранено: {final_name} в {target_dir}")
                return full_path
            else:
                self.log(f"❌ Ошибка вырезания")
                return None
                
        except Exception as e:
            self.log(f"Ошибка: {e}")
            return None
    def clean_url(self, url):
        """Удаляет параметры плейлиста из ссылки"""
        if '&list=' in url:
            url = url.split('&list=')[0]
        # Также удаляем &index= если остался
        if '&index=' in url:
            url = url.split('&index=')[0]    
        return url
    #  --------------------------------------------------------
    #  Chapters
    def get_chapters(self, url):
        """
        Получает список глав (треков) из видео.
        Возвращает список словарей: [{"title": "...", "start": 123.4, "end": 456.7}, ...]
        """
        try:
            # Получаем JSON с информацией о видео
            result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--print-json', url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )
            
            if result.returncode != 0:
                self.log(f"Ошибка получения JSON: {result.stderr}")
                return None
            
            # Парсим JSON
            import json
            data = json.loads(result.stdout)
            
            chapters = data.get('chapters', [])
            if not chapters:
                self.log("Главы (треки) не найдены в видео")
                return None
            
            # Приводим к удобному формату
            tracks = []
            for i, ch in enumerate(chapters, 1):
                tracks.append({
                    "number": i,
                    "title": ch.get('title', f"Трек {i}"),
                    "start_time": ch.get('start_time', 0),
                    "end_time": ch.get('end_time', 0)
                })
            
            self.log(f"Найдено {len(tracks)} треков")
            return tracks
            
        except json.JSONDecodeError as e:
            self.log(f"Ошибка парсинга JSON: {e}")
            return None
        except Exception as e:
            self.log(f"Ошибка получения глав: {e}")
            return None

    def download_track_by_number(self, url, track_number, target_dir):
        """
        Скачивает трек по его порядковому номеру из видео с главами
        """
        tracks = self.get_chapters(url)
        if not tracks:
            return None
        
        if track_number < 1 or track_number > len(tracks):
            self.log(f"Неверный номер трека. Доступно: 1-{len(tracks)}")
            return None
        
        track = tracks[track_number - 1]
        
        # Форматируем время для ffmpeg
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
        else:
            return f"{minutes:02d}:{secs:06.3f}"
    
    start_time = format_time(track["start_time"])
    end_time = format_time(track["end_time"])
    
    # Очищаем название для имени файла
    filename = self.clean_filename(f"{track['number']:02d}_{track['title']}")
    
    self.log(f"Скачивание трека {track['number']}: {track['title']} ({start_time} - {end_time})")
    
    return self.download_clip(url, start_time, end_time, target_dir, filename)
    


def main():
    """Основная функция"""
    
    print("=" * 70)
    print("🎬 YouTube Audio Downloader")
    print(f"📁 Базовый путь: {BASE_MUSIC_DIR}")
    print(f"🍂 Текущий сезон: {paths.get_season_folder()}")
    print("=" * 70)
    
    downloader = YouTubeDownloader()
    
    url = input("\n📎 Ссылка на YouTube: ").strip()
    if not url:
        print("❌ Ссылка не может быть пустой")
        return
    url = downloader.clean_url(url)  # ← добавить
    title, duration = downloader.get_video_info(url)
    if title:
        print(f"📺 Название: {title}")
    if duration:
        print(f"⏱️ Длительность: {duration}")
    
    is_long = downloader.is_long_clip(duration) if duration else False
    
    if is_long:
        print("\n⚠️ Это длинный клип (вероятно, несколько треков)")
        print("1️⃣ Скачать полностью во временную папку (tmp)")
        print("2️⃣ Вырезать один трек сейчас")
        
        choice = input("\nВаш выбор (1/2): ").strip()
        
        if choice == "1":
            result = downloader.download_full(url, downloader.tmp_dir)
            if result:
                print(f"\n✅ Полный клип сохранён в: {result}")
            return
        elif choice == "2":
            start = input("⏱️ Время начала (например 12:34): ").strip()
            end = input("⏱️ Время конца (например 15:45): ").strip()
            custom_name = input("💾 Имя файла (Enter для автоматического): ").strip()
            if not custom_name and title:
                custom_name = downloader.clean_filename(title)
            result = downloader.download_clip(url, start, end, downloader.season_dir, custom_name)
            if result:
                print(f"\n✅ Трек сохранён в сезонную папку")
            return
        else:
            print("❌ Неверный выбор")
            return
    
    else:
        print("\n🎵 Это, вероятно, один трек")
        
        start = input("⏱️ Начало (Enter для 0:00): ").strip()
        if not start:
            start = "0:00"
        
        end = input("⏱️ Конец (Enter для полной длины): ").strip()
        
        custom_name = input("💾 Имя файла (Enter для автоматического): ").strip()
        if not custom_name and title:
            custom_name = downloader.clean_filename(title)
        
        if end:
            result = downloader.download_clip(url, start, end, downloader.season_dir, custom_name)
        else:
            result = downloader.download_full(url, downloader.season_dir, custom_name)
        
        if result:
            print(f"\n✅ Трек сохранён в сезонную папку")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")