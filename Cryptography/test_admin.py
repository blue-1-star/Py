import os
import ctypes
import sys

def is_admin():
    """Проверяет, запущен ли Python от имени администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

print(f"Запущено от админа: {is_admin()}")
# Если False - даже при наличии прав админа, нужно перезапустить