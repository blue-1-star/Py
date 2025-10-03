import subprocess

# Выполнить команду pip freeze для системной версии Python
def get_global_packages(output_file):
    try:
        with open(output_file, 'w') as f:
            subprocess.check_call(['pip', 'freeze'], stdout=f)
        print(f"Список глобальных библиотек сохранен в {output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")

# Укажите путь для сохранения файла
output_path = r'G:\Programming\Py\all_installed_packages.txt'

# get_global_packages(output_path)
# "C:\Python\python.exe"      # Python 3.11
#  "C:\Program Files\Python313\python.exe"    # Python 3.13   