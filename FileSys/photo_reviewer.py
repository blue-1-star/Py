import os
import json
from datetime import datetime
from pathlib import Path

class PhotoStorageObserver:
    # def __init__(self, root_directory, log_file="storage_log.json"):
    #     self.root_directory = root_directory
    #     self.log_file = log_file
    def __init__(self, root_directory):
        self.root_directory = Path(root_directory)
        self.log_file = self.root_directory / "storage_log.json"  # Лог-файл в этой папке
        self.current_state = {}

        # Загружаем существующий журнал, если он есть
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.journal = json.load(f)
        else:
            self.journal = {}

    def scan_directory(self):
        """Сканирует каталог и возвращает его состояние в виде словаря."""
        state = {}
        for dirpath, dirnames, filenames in os.walk(self.root_directory):
            rel_path = os.path.relpath(dirpath, self.root_directory)
            state[rel_path] = {
                "directories": sorted(dirnames),
                "files": sorted(filenames)
            }
        return state

    def detect_changes(self):
        """Сравнивает текущее состояние каталога с предыдущим."""
        self.current_state = self.scan_directory()
        if not self.journal:
            return {"added_dirs": [], "added_files": [], "removed_dirs": [], "removed_files": []}

        last_state = self.journal.get("last_state", {})
        added_dirs, removed_dirs = self._compare_keys(last_state, self.current_state, key_type="directories")
        added_files, removed_files = self._compare_keys(last_state, self.current_state, key_type="files")
        return {
            "added_dirs": added_dirs,
            "added_files": added_files,
            "removed_dirs": removed_dirs,
            "removed_files": removed_files
        }

    def _compare_keys(self, last_state, current_state, key_type):
        """Сравнивает ключи (директории или файлы) между состояниями."""
        added = []
        removed = []

        for path, content in current_state.items():
            if path in last_state:
                current_keys = set(content[key_type])
                last_keys = set(last_state[path][key_type])
                added.extend([(path, item) for item in current_keys - last_keys])
                removed.extend([(path, item) for item in last_keys - current_keys])
            else:
                added.extend([(path, item) for item in content[key_type]])

        for path, content in last_state.items():
            if path not in current_state:
                removed.extend([(path, item) for item in content[key_type]])

        return added, removed

    def log_changes(self):
        """Логирует текущие изменения и сохраняет их в журнал."""
        changes = self.detect_changes()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.journal[timestamp] = changes
        self.journal["last_state"] = self.current_state

        with open(self.log_file, "w") as f:
            json.dump(self.journal, f, indent=4)

        return changes

    def get_report(self, date=None):
        """Возвращает журнал или отчет на указанную дату."""
        if date:
            return self.journal.get(date, "Нет данных за указанную дату.")
        return self.journal

    def detailed_report(self, state=None):
        """Возвращает детализированный отчет по текущему состоянию или указанному."""
        state = state or self.current_state
        report = []
        for dir_path, content in state.items():
            report.append(f"Каталог: {dir_path}")
            report.append(f"  Подкаталоги: {', '.join(content['directories']) if content['directories'] else 'Нет'}")
            report.append(f"  Файлы: {', '.join(content['files']) if content['files'] else 'Нет'}")
        return "\n".join(report)


# Пример использования
if __name__ == "__main__":
    rd = 'g:/test/'
    observer = PhotoStorageObserver(root_directory=rd)

    # Сканировать и записать изменения
    changes = observer.log_changes()
    print("Изменения:", changes)

    # Получить детализированный отчет
    print("Текущий отчет:")
    print(observer.detailed_report())

    # Получить журнал за указанную дату
    print("Журнал:")
    print(observer.get_report())
