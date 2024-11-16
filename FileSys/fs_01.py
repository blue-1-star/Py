
import os
import platform
from pathlib import Path
p = Path('.')
ld= [x for x in p.iterdir() if x.is_dir()]
print(ld)
# dir_v = os.listdir("G:/Photo/OnePlus/Video/")
# dir_v = os.listdir("G:/test/1/")
dir_v = os.listdir("G:/test/")
# dir_p = os.listdir("G:/test/2/")
print(dir_v)

print(os.cpu_count())
print(os.getcwd())
os.chdir("g:/test")
print(os.getcwd())
print(os.getlogin())
# os.makedirs("g:/test/w3school")
# output = os.environ['HOME']
# os.rmdir("w3school")
print(platform.uname())


# Создаём объект Path для текущего каталога
current_dir = Path('.')

# Разделяем содержимое на файлы и папки
folders = [x.name for x in current_dir.iterdir() if x.is_dir()]
files = [x.name for x in current_dir.iterdir() if x.is_file()]

# Выводим результат
print("FOLDERS:")
print(", ".join(folders) if folders else "No folders")
print("\nFILES:")
print(", ".join(files) if files else "No files")







