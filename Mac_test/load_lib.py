import sys
import os
import pandas  # если установлен

print(f"sys загружен из: {sys.__file__}")
# sys загружен из: /usr/local/lib/python3.12/sys.py

print(f"os загружен из: {os.__file__}")
# os загружен из: /usr/local/lib/python3.12/os.py

try:
    print(f"pandas загружен из: {pandas.__file__}")
    # pandas загружен из: /venv/lib/python3.12/site-packages/pandas/__init__.py
except NameError:
    print("pandas не установлен")