import os
import shutil
import re

def safe_move(src, dest):
    """
    Безопасно перемещает файл: копирует файл из src в dest, 
    проверяет успешность копирования и только затем удаляет исходный файл.
    """
    try:
        shutil.copy2(src, dest)
        if os.path.exists(dest):
            os.remove(src)
        else:
            print(f"Ошибка: не удалось скопировать файл {src} в {dest}")
    except Exception as e:
        print(f"Ошибка при перемещении файла {src} в {dest}: {e}")

def organize_photos(input_dir):
    """
    Организует фотографии в каталоге input_dir согласно следующему алгоритму:
      1. Если в названии файла встречается "best", перемещает файл в подкаталог best.
         Если встречается "worst" – в подкаталог worst.
      2. В каждом из подкаталогов (best, worst) создаются вложенные подкаталоги "4x", "10x" и "40x"
         в зависимости от наличия соответствующей подстроки в имени файла, и файл перемещается туда.
    
    Порядок действий:
      - Для каждого файла из input_dir (без рекурсии) проверяется имя.
      - Сначала файлы копируются в подкаталог best или worst (с последующим удалением исходного файла).
      - Затем в каждом из этих подкаталогов производится поиск подстрок "4x", "10x" или "40x"
        и файлы перемещаются во вложенные подкаталоги.
    """
    # Создаем подкаталоги best и worst в каталоге input_dir, если их нет
    best_dir = os.path.join(input_dir, "best")
    worst_dir = os.path.join(input_dir, "worst")
    os.makedirs(best_dir, exist_ok=True)
    os.makedirs(worst_dir, exist_ok=True)
    
    # Шаг 1: Распределяем файлы из input_dir в подкаталоги best и worst
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        # Обрабатываем только файлы (пропускаем подкаталоги)
        if os.path.isfile(file_path):
            lower_name = filename.lower()
            if "best" in lower_name:
                dest_path = os.path.join(best_dir, filename)
                safe_move(file_path, dest_path)
            elif "worst" in lower_name:
                dest_path = os.path.join(worst_dir, filename)
                safe_move(file_path, dest_path)
    
    # Шаг 2: В подкаталогах best и worst создаем вложенные подкаталоги по меткам "4x", "10x", "40x"
    for parent_dir in [best_dir, worst_dir]:
        # Получаем список файлов в текущем подкаталоге
        for filename in os.listdir(parent_dir):
            file_path = os.path.join(parent_dir, filename)
            if os.path.isfile(file_path):
                lower_name = filename.lower()
                # Проверяем наличие каждой из меток
                for tag in ["4x", "10x", "40x"]:
                    if tag in lower_name:
                        # Создаем вложенный подкаталог tag, если он еще не существует
                        tag_dir = os.path.join(parent_dir, tag)
                        os.makedirs(tag_dir, exist_ok=True)
                        dest_path = os.path.join(tag_dir, filename)
                        safe_move(file_path, dest_path)
                        # Если найден один тег – прекращаем проверку для данного файла
                        break

# Пример вызова функции:
organize_photos(r"G:\My\sov\extract\Spores\original_img")

