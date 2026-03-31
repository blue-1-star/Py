# config.py (в корне Py/)
from pathlib import Path
import platform
from datetime import datetime

class ProjectPaths:
    def __init__(self, project_root=None):
        self.os_name = platform.system()
        self.home = Path.home()
        
        if self.os_name == "Windows":
            self.EXTERNAL_DRIVE = Path("D:/")
        elif self.os_name == "Darwin":
            self.EXTERNAL_DRIVE = Path("/Volumes/microSD256")
        else:
            self.EXTERNAL_DRIVE = Path("/mnt/external")
        
        self.BASE_MUSIC_DIR = self.EXTERNAL_DRIVE / "Music" / "fav"
        self.TMP_DIR = self.BASE_MUSIC_DIR / "tmp"
        self.LOG_DIR = self.BASE_MUSIC_DIR / "log"
        
        if project_root:
            self.PROJECT_ROOT = Path(project_root).resolve()
        else:
            self.PROJECT_ROOT = Path.cwd()
        
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.ONEDRIVE = self._get_onedrive_path()
        self.FLAT_FILE = self.ONEDRIVE / "Flat_Arn.xlsx"
        self.DOCUMENTS = self.ONEDRIVE / "Документы"
        self.inp_dir = str(self.ONEDRIVE)
    
    def _get_onedrive_path(self):
        if self.os_name == "Windows":
            return Path("D:/OneDrive/Документы")
        else:
            return self.home / "Library/CloudStorage/OneDrive-Personal"
    
    def get_season_folder(self):
        """Определяет сезонную папку по дате"""
        now = datetime.now()          # ← ЭТО КЛЮЧЕВАЯ СТРОКА!
        year = now.year
        month = now.month
        day = now.day
        
        if 3 <= month <= 5:
            return f"{year}_spring"
        elif 6 <= month <= 8:
            return f"{year}_summer"
        elif (9 <= month <= 11) or (month == 12 and day <= 14):
            return f"{year}_autumn"
        else:
            if month == 12 and day >= 15:
                return f"{year + 1}_winter"
            else:
                return f"{year}_winter"
    
    def get_current_season_dir(self):
        return self.BASE_MUSIC_DIR / self.get_season_folder()
    
    def ensure_directories(self):
        dirs = [
            self.get_current_season_dir(),
            self.TMP_DIR,
            self.LOG_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return self.get_current_season_dir()
    
    def get_log_file(self):
        today = datetime.now().strftime("%Y%m%d")
        return self.LOG_DIR / f"download_{today}.txt"


# ✅ СОЗДАЁМ ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР
paths = ProjectPaths()
print("✅ config.py загружен успешно")