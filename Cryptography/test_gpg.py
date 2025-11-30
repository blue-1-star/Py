# Простой тест GPG
import subprocess
import getpass

# Константы
KEY_FILE_NAME = "backup_2025-11-23.sec.pgp"  # измените на имя вашего файла
GPG_PATH = r"C:\Program Files (x86)\GnuPG\bin\gpg.exe"

def run_gpg_command(args):
    """Запускает GPG команду с явным указанием пути"""
    full_cmd = [GPG_PATH] + args
    print(f"🔧 Выполняется: {' '.join(full_cmd)}")
    
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return None

def test_gpg():
    result = run_gpg_command(['--version'])
    if result and result.returncode == 0:
        print("✅ GPG работает корректно!")
        print(result.stdout)
    else:
        print("❌ Проблема с GPG")

test_gpg()