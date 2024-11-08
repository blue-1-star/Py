import os 
path = '/home/User/Desktop/file.txt'
root_ext = os.path.splitext(path) 
print("root part of '% s':" % path, root_ext[0]) 
print("ext part of '% s':" % path, root_ext[1], "\n") 

from datetime import datetime
now = datetime.now() # поточна дата та час
year = now.strftime("%Y")
print("year:", year)
 
month = now.strftime("%m")
print("month:", month)
 
day = now.strftime("%d")
print("day:", day)
 
time = now.strftime("%H:%M:%S")
print("time:", time)
 
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)
date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
print("date and time:",date_time)