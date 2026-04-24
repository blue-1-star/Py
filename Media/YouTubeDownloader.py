#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re
import json
import sys
from datetime import datetime
from pathlib import Path

# Добавляем корневую папку Py/ в путь поиска модулей
PY_ROOT = Path(__file__).parent.parent  # поднимаемся из Media/ в Py/
sys.path.insert(0, str(PY_ROOT))

# Теперь импорт сработает
from config import paths
# Импортируем наш класс путей (если используешь config.py)
try:
    from config import paths
    print(f"✅ config.py загружен, диск: {paths.EXTERNAL_DRIVE}")
except ImportError as e:
    print(f"⚠️ config.py не найден: {e}")
    # Если config.py нет, создаём базовые пути
    class SimplePaths:
        def __init__(self):
            self.BASE_MUSIC_DIR = Path.home() / "Music" / "fav"
            self.TMP_DIR = self.BASE_MUSIC_DIR / "tmp"
            self.LOG_DIR = self.BASE_MUSIC_DIR / "log"
    paths = SimplePaths()


class YouTubeDownloader:
    """Класс для скачивания треков с YouTube с поддержкой глав"""
    
    def __init__(self, save_dir=None):
        """Инициализация загрузчика"""
        if save_dir:
            self.save_dir = Path(save_dir)
        else:
            self.season_dir = paths.ensure_directories() if hasattr(paths, 'ensure_directories') else paths.BASE_MUSIC_DIR
            self.tmp_dir = paths.TMP_DIR if hasattr(paths, 'TMP_DIR') else paths.BASE_MUSIC_DIR / "tmp"
            self.log_dir = paths.LOG_DIR if hasattr(paths, 'LOG_DIR') else paths.BASE_MUSIC_DIR / "log"
        
        # Создаём папки
        if hasattr(paths, 'ensure_directories'):
            self.season_dir = paths.ensure_directories()
            self.tmp_dir = paths.TMP_DIR
            self.log_dir = paths.LOG_DIR
        else:
            self.season_dir = save_dir or paths.BASE_MUSIC_DIR
            self.tmp_dir = self.season_dir / "tmp"
            self.log_dir = self.season_dir / "log"
        
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Файл лога (один общий)
        self.log_file = self.log_dir / "download_history.log"
        self._init_log_file()
    
    def _init_log_file(self):
        """Инициализирует файл лога с заголовком"""
        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("# Журнал скачиваний YouTubeDownloader\n")
                f.write("# Формат: [ДАТА] | СТАТУС | ИМЯ_ФАЙЛА | ИСТОЧНИК\n")
                f.write("#" * 80 + "\n")
    
    def log(self, message, to_file=True):
        """Записывает сообщение в консоль и (опционально) в лог"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        if to_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + '\n')
            except Exception as e:
                print(f"Ошибка записи лога: {e}")
    
    def log_success(self, filename, source_url=None, track_info=None):
        """Записывает только успешные скачивания в специальный формат"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Формируем строку лога
        log_entry = f"[{timestamp}] | УСПЕХ | {filename}"
        
        if track_info:
            log_entry += f" | {track_info.get('title', '')} (#{track_info.get('number', '?')})"
        elif source_url:
            short_url = source_url.split('&')[0][:50] + "..." if len(source_url) > 60 else source_url
            log_entry += f" | {short_url}"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Ошибка записи лога: {e}")
    
    def clean_filename(self, title):
        """Очищает название файла от недопустимых символов, сохраняя пробелы"""
        # Удаляем запрещённые символы для имен файлов
        clean = re.sub(r'[<>:"/\\|?*]', '', title)
        # Заменяем последовательности подчёркиваний на пробелы
        clean = re.sub(r'_+', ' ', clean)
        # Сжимаем любые пробельные символы в один пробел
        clean = re.sub(r'\s+', ' ', clean)
        clean = clean.strip()
        # Ограничиваем длину
        if len(clean) > 80:
            clean = clean[:77] + "..."
        return clean
    
    def get_video_info(self, url, timeout=60):
        """Получает информацию о видео: название, длительность"""
        try:
            # Очищаем URL от параметров плейлиста
            clean_url = self._clean_url(url)
            
            # Получаем название
            title_result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--get-title', clean_url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            original_title = title_result.stdout.strip() if title_result.returncode == 0 else None
            
            # Получаем длительность
            duration_result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--get-duration', clean_url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            duration = duration_result.stdout.strip() if duration_result.returncode == 0 else None
            
            return original_title, duration
            
        except subprocess.TimeoutExpired:
            self.log(f"Таймаут при получении информации для {url}")
            return None, None
        except Exception as e:
            self.log(f"Ошибка получения информации: {e}")
            return None, None
    
    def _clean_url(self, url):
        """Удаляет параметры плейлиста из ссылки"""
        if '&list=' in url:
            url = url.split('&list=')[0]
        if '&index=' in url:
            url = url.split('&index=')[0]
        return url
    
    # 
    def get_chapters(self, url, timeout=120):
        """
        Получает список глав (треков) из видео.
        Сначала пытается через JSON, если не получается — парсит описание.
        """
        try:
            clean_url = self._clean_url(url)
            
            # СПОСОБ 1: Через JSON
            result = subprocess.run(
                ['yt-dlp', '--remote-components', 'ejs:github', '--print-json', clean_url],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            
            chapters = []
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                chapters = data.get('chapters', [])
            
            # СПОСОБ 2: Если JSON не дал глав — парсим описание
            if not chapters:
                self.log("JSON не дал глав, пробуем парсить описание...")
                
                # Получаем описание видео
                desc_result = subprocess.run(
                    ['yt-dlp', '--remote-components', 'ejs:github', '--get-description', clean_url],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=timeout
                )
                
                if desc_result.returncode == 0:
                    description = desc_result.stdout
                    chapters = self._parse_chapters_from_description(description)
            
            if not chapters:
                self.log("Главы (треки) не найдены в видео")
                return None
            
            # Приводим к удобному формату
            tracks = []
            for i, ch in enumerate(chapters, 1):
                title = ch.get('title', f"Трек {i}")
                clean_title = self.clean_filename(title)
                
                tracks.append({
                    "number": i,
                    "title": clean_title,
                    "original_title": title,
                    "start_time": ch.get('start_time', 0),
                    "end_time": ch.get('end_time', 0)
                })
            
            self.log(f"Найдено {len(tracks)} треков с главами")
            return tracks
            
        except Exception as e:
            self.log(f"Ошибка получения глав: {e}")
            return None

    def _parse_chapters_from_description(self, description):
        """
        Парсит главы из текста описания видео.
        Ищет строки вида "0:00 Название" или "00:00 Название"
        """
        import re
        
        chapters = []
        lines = description.split('\n')
        
        # Регулярное выражение для поиска таймкодов в начале строки
        # Форматы: 0:00, 00:00, 1:23:45
        pattern = re.compile(r'^(\d{1,2}:)?\d{1,2}:\d{2}\s+(.+)$')
        
        previous_time = 0
        previous_title = None
        
        for line in lines:
            line = line.strip()
            match = pattern.match(line)
            if match:
                # Извлекаем время и название
                time_str = match.group(0)
                # Отделяем время от названия
                parts = time_str.split(maxsplit=1)
                if len(parts) == 2:
                    time_part, title = parts
                    # Преобразуем время в секунды
                    seconds = self._time_to_seconds(time_part)
                    
                    # Если это не первый трек, добавляем предыдущий с вычисленным end_time
                    if previous_title is not None:
                        chapters[-1]['end_time'] = seconds
                    
                    chapters.append({
                        'title': title,
                        'start_time': seconds,
                        'end_time': 0  # временно, будет заполнено следующим треком
                    })
                    previous_title = title
                    previous_time = seconds
        
        # Для последнего трека end_time не определён
        # Можно установить как start_time + (средняя длительность) или оставить 0
        if chapters and chapters[-1]['end_time'] == 0:
            # Если это последний трек, установим end_time как start_time + 5 минут (примерно)
            # Лучше потом вручную скорректировать
            chapters[-1]['end_time'] = chapters[-1]['start_time'] + 300  # +5 минут
        
        return chapters

    def _time_to_seconds(self, time_str):
        """Преобразует строку времени (MM:SS или HH:MM:SS) в секунды"""
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    def _format_time(self, seconds):
        """Преобразует секунды в формат времени HH:MM:SS.mmm или MM:SS.mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
        else:
            return f"{minutes:02d}:{secs:06.3f}"
    
    def download_clip(self, url, start_time, end_time, target_dir, filename=None):
        """Скачивает и вырезает фрагмент"""
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Определяем имя файла
        if not filename:
            title, _ = self.get_video_info(url)
            if title:
                base_name = self.clean_filename(title)
            else:
                base_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            base_name = filename
        
        # Проверяем, нет ли файла с таким именем
        full_path = target_dir / f"{base_name}.mp3"
        counter = 1
        while full_path.exists():
            full_path = target_dir / f"{base_name}_{counter}.mp3"
            counter += 1
        
        clean_url = self._clean_url(url)
        
        self.log(f"Вырезание фрагмента {start_time} - {end_time} -> {full_path.name}")
        
        command = [
            'yt-dlp',
            '--remote-components', 'ejs:github',
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--postprocessor-args', f'-ss {start_time} -to {end_time}',
            '-o', str(full_path),
            clean_url
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
                self.log_success(full_path.name, url)
                return full_path
            else:
                self.log(f"Ошибка вырезания")
                return None
                
        except Exception as e:
            self.log(f"Ошибка: {e}")
            return None
    
    def download_full(self, url, target_dir, filename=None):
        """Скачивает полное видео/аудио целиком"""
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            title, _ = self.get_video_info(url)
            if title:
                base_name = self.clean_filename(title)
            else:
                base_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            base_name = filename
        
        full_path = target_dir / f"{base_name}.mp3"
        counter = 1
        while full_path.exists():
            full_path = target_dir / f"{base_name}_{counter}.mp3"
            counter += 1
        
        clean_url = self._clean_url(url)
        
        self.log(f"Скачивание полного файла: {full_path.name}")
        
        command = [
            'yt-dlp',
            '--remote-components', 'ejs:github',
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', str(full_path),
            clean_url
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
                self.log_success(full_path.name, url)
                return full_path
            else:
                self.log(f"Ошибка скачивания")
                return None
                
        except Exception as e:
            self.log(f"Ошибка: {e}")
            return None
    
    def download_track_by_number(self, url, track_number, target_dir):
        """
        Скачивает трек по его порядковому номеру из видео с главами
        """
        tracks = self.get_chapters(url)
        if not tracks:
            self.log("Не удалось получить список треков")
            return None
        
        if track_number < 1 or track_number > len(tracks):
            self.log(f"Неверный номер трека. Доступно: 1-{len(tracks)}")
            return None
        
        track = tracks[track_number - 1]
        
        start_time = self._format_time(track["start_time"])
        end_time = self._format_time(track["end_time"])
        
        # Используем название трека для имени файла
        filename = f"{track['number']:02d}_{track['title']}"
        
        self.log(f"Скачивание трека {track['number']}: {track['title']} ({start_time} - {end_time})")
        
        return self.download_clip(url, start_time, end_time, target_dir, filename)
    
    def list_tracks(self, url):
        """Выводит список всех треков из видео с главами"""
        tracks = self.get_chapters(url)
        if not tracks:
            print("Треки не найдены")
            return None
        
        print("\n" + "=" * 60)
        print(f"📋 Найдено треков: {len(tracks)}")
        print("=" * 60)
        
        for track in tracks:
            start = self._format_time(track["start_time"])
            end = self._format_time(track["end_time"])
            print(f"{track['number']:2d}. {start} - {end} : {track['title']}")
        
        print("=" * 60)
        return tracks


# Пример использования
def main():
    print("=" * 70)
    print("🎬 YouTube Audio Downloader с поддержкой глав")
    print("=" * 70)
    
    downloader = YouTubeDownloader()
    
    url = input("\n📎 Ссылка на YouTube: ").strip()
    if not url:
        print("❌ Ссылка не может быть пустой")
        return
    
    # Пытаемся получить главы
    tracks = downloader.list_tracks(url)
    
    if tracks:
        print("\nВыберите действие:")
        print("1️⃣  Скачать один трек по номеру")
        print("2️⃣  Скачать все треки")
        print("3️⃣  Скачать как обычно (без глав)")
        
        choice = input("\nВаш выбор (1/2/3): ").strip()
        
        if choice == "1":
            track_num = int(input("Номер трека: ").strip())
            downloader.download_track_by_number(url, track_num, downloader.season_dir)
        elif choice == "2":
            for track in tracks:
                print(f"\n--- Скачивание трека {track['number']}: {track['title']} ---")
                downloader.download_track_by_number(url, track['number'], downloader.season_dir)
        else:
            # Обычное скачивание
            start = input("⏱️ Начало (Enter для 0:00): ").strip() or "0:00"
            end = input("⏱️ Конец (Enter для полной длины): ").strip()
            custom_name = input("💾 Имя файла (Enter для автоматического): ").strip()
            filename = custom_name if custom_name else None
            
            if end:
                downloader.download_clip(url, start, end, downloader.season_dir, filename)
            else:
                downloader.download_full(url, downloader.season_dir, filename)
    else:
        # Обычное скачивание (без глав)
        print("\n🎵 Треки не найдены, обычное скачивание")
        start = input("⏱️ Начало (Enter для 0:00): ").strip() or "0:00"
        end = input("⏱️ Конец (Enter для полной длины): ").strip()
        custom_name = input("💾 Имя файла (Enter для автоматического): ").strip()
        filename = custom_name if custom_name else None
        
        if end:
            downloader.download_clip(url, start, end, downloader.season_dir, filename)
        else:
            downloader.download_full(url, downloader.season_dir, filename)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")