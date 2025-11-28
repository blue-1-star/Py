import os
import subprocess

def check_gpg_installed():
    """Проверяет установлен ли GPG"""
    try:
        result = subprocess.run(['gpg', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

if not check_gpg_installed():
    print("❌ GPG не установлен!")
    print("📥 Скачайте и установите Gpg4win:")
    print("   https://www.gpg4win.org/")
    print("Или используйте альтернативные методы ниже")