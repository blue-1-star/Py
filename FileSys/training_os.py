# Метод datetime.strftime() в Python   https://acode.com.ua/method-strftime-python/
# Метод datetime.strptime() в Python   https://acode.com.ua/method-strptime-python/
import os
from datetime import datetime
# import locale 
# locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
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

uk_months = {
    "січень": "January",
    "лютий": "February",
    "березень": "March",
    "квітень": "April",
    "травень": "May",
    "червень": "June",
    "липень": "July",
    "серпень": "August",
    "вересень": "September",
    "жовтень": "October",
    "листопад": "November",
    "грудень": "December"
}
# Словарь со всеми возможными формами месяцев
uk_months = {
    "січень": "January", "січня": "January",
    "лютий": "February", "лютого": "February",
    "березень": "March", "березня": "March",
    "квітень": "April", "квітня": "April",
    "травень": "May", "травня": "May",
    "червень": "June", "червня": "June",
    "липень": "July", "липня": "July",
    "серпень": "August", "серпня": "August",
    "вересень": "September", "вересня": "September",
    "жовтень": "October", "жовтня": "October",
    "листопад": "November", "листопада": "November",
    "грудень": "December", "грудня": "December"
}
# Функция для замены украинских форм на английские
def replace_uk_months(date_string, months_dict):
    for ukr, eng in months_dict.items():
        if ukr in date_string:
            return date_string.replace(ukr, eng)
    return date_string

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)
date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
print("date and time:",date_time)
date_string = "21 June, 2018"
date_string_u = "9 листопад, 2024"
for ukr, eng in uk_months.items():
    if ukr in date_string_u:
        date_string_u = date_string_u.replace(ukr, eng)
        break
print("date_string =", date_string)
print("date_string_u =", date_string_u)
print("type of date_string =", type(date_string))
print("type of date_string_u =", type(date_string_u))
date_object = datetime.strptime(date_string, "%d %B, %Y")
date_object_u = datetime.strptime(date_string_u, "%d %B, %Y")
print("date_object =", date_object)
print("date_object_u =", date_object_u)
print("type of date_object =", type(date_object))
print("type of date_object =", type(date_object_u))
print("-----------------------------")

date_strings_u = ["9 листопад, 2024", "15 січня, 2022", "25 грудня, 2023"]

for date_string_u in date_strings_u:
    date_string_u_eng = replace_uk_months(date_string_u, uk_months)
    date_object_u = datetime.strptime(date_string_u_eng, "%d %B, %Y")
    print(f"Украинская дата: {date_string_u} -> Английская дата: {date_object_u} -> Объект: {date_object_u}")
