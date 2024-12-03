import os
def get_full_file_path(filename):
    """
    Возвращает полный путь к файлу данных, находящемуся в той же директории,
    что и текущий скрипт, или в указанной поддиректории.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
    return os.path.join(script_dir, filename)

script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
print(os.path.dirname(os.path.abspath(__file__)))    
