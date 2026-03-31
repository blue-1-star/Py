import sys
import os

# Безопасная функция для получения информации о модуле
def get_module_info(module):
    """Возвращает информацию об источнике модуля"""
    module_name = module.__name__
    
    # Проверяем, встроенный ли модуль
    if module_name in sys.builtin_module_names:
        return f"[встроенный модуль] {module_name}"
    
    # Пытаемся получить __file__
    if hasattr(module, '__file__') and module.__file__:
        return module.__file__
    
    # Пробуем через spec
    if hasattr(module, '__spec__') and module.__spec__ and module.__spec__.origin:
        return module.__spec__.origin
    
    return "[источник не определён]"

# Теперь безопасно выводим информацию
print(f"sys загружен из: {get_module_info(sys)}")
# Результат: sys загружен из: [встроенный модуль] sys

print(f"os загружен из: {get_module_info(os)}")
# Результат: os загружен из: /usr/local/lib/python3.12/os.py

# Проверяем pandas (если установлен)
try:
    import pandas
    print(f"pandas загружен из: {get_module_info(pandas)}")
    # Результат: pandas загружен из: /venv/lib/python3.12/site-packages/pandas/__init__.py
except ImportError:
    print("pandas не установлен")

# Дополнительно: покажем все встроенные модули
print(f"\nВсе встроенные модули: {', '.join(sorted(sys.builtin_module_names)[:10])}...")