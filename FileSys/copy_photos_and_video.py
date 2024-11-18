import os
import shutil
import datetime
import time
import subprocess
from pathlib import Path
import pytz
import lib_photos
from lib_photos import copy_photos_by_date, get_creation_date,  get_video_creation_date, copy_and_delete_photos_by_date

# Пример использования
source_directory = 'g:/test'
target_directory = 'g:/test/imvers'
copy_photos_by_date(source_directory, target_directory)
# copy_and_delete_photos_by_date(source_directory, target_directory)
