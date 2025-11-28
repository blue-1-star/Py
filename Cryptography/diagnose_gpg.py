import subprocess
import os

def diagnose_gpg():
    """Диагностика где находится GPG"""
    print("🔍 ДИАГНОСТИКА GPG...")
    
    # Проверяем разные возможные расположения
    possible_paths = [
        r"C:\Program Files (x86)\GnuPG\bin\gpg.exe",
        r"C:\Program Files\GnuPG\bin\gpg.exe", 
        r"C:\Program Files\Gpg4win\bin\gpg.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Gpg4win\bin\gpg.exe")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Найден: {path}")
            return path
        else:
            print(f"❌ Не найден: {path}")
    
    # Ищем в PATH
    try:
        result = subprocess.run(['where', 'gpg'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Найден через PATH: {result.stdout.strip()}")
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    print("❌ GPG не найден в стандартных местах")
    return None

gpg_path = diagnose_gpg()