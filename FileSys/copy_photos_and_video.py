import os
import shutil
import datetime
import time
import subprocess
from pathlib import Path
import pytz
import lib_photos
from lib_photos import copy_photos_by_date, get_creation_date,  get_video_creation_date, copy_and_delete_photos_by_date, \
    copy_photos_by_date_st_end

# Пример использования
# source_directory = 'g:/test'
source_directory = r"G:\Photo\OnePlus\Photo"
# target_directory = 'g:/test/imvers'
# r"G:\Photo\OnePlus\Photo"
target_directory = r"G:\Photo\OnePlus\Photo"
# copy_photos_by_date(source_directory, target_directory)
start_date = datetime.date(2024, 10, 30 )
end_date = datetime.date(2024, 10, 30)
# copy_photos_by_date_st_end(source_directory, target_directory, start_date, end_date)
copy_photos_by_date_st_end(source_directory, target_directory, start_date)
# copy_and_delete_photos_by_date(source_directory, target_directory)
