import subprocess
import os
import sys

# Путь к старой версии Python
old_python_path = r"C:\Python\python.exe"  # Замените на путь к вашей старой Python

# Пути к файлам
old_req_file = 'old_requirements.txt'
new_req_file = 'new_requirements.txt'
diff_file = 'diff_old_minus_new.txt'

def get_packages(python_path, output_file):
    """Получить список установленных пакетов из указанного Python."""
    with open(output_file, 'w') as f:
        subprocess.check_call([python_path, '-m', 'pip', 'freeze'], stdout=f)

def main():
    print("Получение списка пакетов из старой версии Python...")
    get_packages(old_python_path, old_req_file)

    print("Получение списка пакетов из текущего активного окружения...")
    get_packages(sys.executable, new_req_file)

    # Загружаем списки в множества
    with open(old_req_file) as f:
        old_libs = set(line.strip() for line in f if line.strip())

    with open(new_req_file) as f:
        new_libs = set(line.strip() for line in f if line.strip())

    # Вычисляем разность
    libs_to_install = old_libs - new_libs

    # Записываем результат
    with open(diff_file, 'w') as f:
        for lib in sorted(libs_to_install):
            f.write(lib + '\n')

    print(f"Список библиотек (в старом, но отсутствующих в новом): {diff_file}")

if __name__ == '__main__':
    main()
