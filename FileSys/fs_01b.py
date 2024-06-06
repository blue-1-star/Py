# import os
# import shutil
# import datetime
# import time
# import subprocess
# from lib_photos import get_creation_date, get_video_creation_date, copy_photos_by_date
from lib_photos import  copy_photos_by_date

# Пример использования
source_directory = 'g:/test'
target_directory = 'g:/test/imvers'
copy_photos_by_date(source_directory, target_directory)
