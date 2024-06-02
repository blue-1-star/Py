
import os
import platform
from pathlib import Path
p = Path('.')
ld= [x for x in p.iterdir() if x.is_dir()]
# print(ld)
dir_v = os.listdir("G:/Photo/OnePlus/Video/")
dir_p = os.listdir("G:/Photo/OnePlus/Photo/")
print(dir_v)

# print(os.cpu_count())
# print(os.getcwd())
os.chdir("g:/test")
print(os.getcwd())
# print(os.getlogin())
# os.makedirs("g:/test/w3school")
# output = os.environ['HOME']
os.rmdir("w3school")
# print(platform.uname())







