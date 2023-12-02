# ЗАГРУЗКА ДАННЫХ
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
sp500 = pd.read_csv("G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\sp500.csv",
index_col='Symbol',
usecols=[0, 2, 3, 7])
omh = pd.read_csv("G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\omh.csv")
import csv
str_data = "G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\msft.csv"
dir_dat = "G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\"
with open(str_data) as file:
    reader = csv.reader(file, delimiter=',')
    for i,row in enumerate(reader):
        print(row)
        if(i >= 5):
            break
# считываем msft.csv в датафрейм
# msft = pd.read_csv(str_data)
msft = pd.read_csv(str_data, index_col=0)
print(msft[:5])
# исследуем типы столбцов в этом датафрейме
print(msft.dtypes)
msft = pd.read_csv(str_data, index_col=0,dtype = { 'Volume' : np.float64})
print(msft.dtypes)
# задаем новый набор имен для столбцов
# все имеют нижний регистр,
# header=0 задает строку заголовков
df = pd.read_csv(str_data, header=0,names=['date', 'open', 'high', 'low',
'close', 'volume'])
print(df[:5])
df2 = pd.read_csv(str_data, usecols=['Date', 'Close'],
index_col=['Date'])
print(df2[:5])
file = "msft_modified.csv"
df2.to_csv(dir_dat+file, index_label='date')
# ------------    191
# задаем URL-адрес HTML-файла
# url = "http://www.fdic.gov/bank/individual/failed/banklist.html"
url= "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/"
# читаем его
banks = pd.read_html(url)
# проверяем, как была прочитана
# часть первой таблицы
print(banks[0][0:5].iloc[:,0:2])
#  pip install lxml
# lxml-4.9.3
# pip install html5lib
# Successfully installed html5lib-1.1 webencodings-0.5.1
# pip install beautifulsoup4
# Successfully installed beautifulsoup4-4.12.2 soupsieve-2.5
# считываем данные о котировках акций
file1 ="stocks.xlsx" 
df = pd.read_excel(dir_dat+file1)
# записываем первые две строки в HTML
df.head(2).to_html(dir_dat + "stocks.html")
# смотрим HTML-файл в браузере
import webbrowser
# webbrowser.open(dir_dat + "stocks.html")
# -------------------------------------------------    194
# считываем csv непосредственно по URL-адресу
countries = pd.read_csv(
"https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv")
print(countries[:5])
#   SQL   
# импортируем библиотеку SQLite
import sqlite3
msft = pd.read_csv(dir_dat+"msft.csv")
msft["Symbol"]="MSFT"
aapl = pd.read_csv(dir_dat+"aapl.csv")
aapl["Symbol"]="AAPL"
connection = sqlite3.connect(dir_dat+"stocks.sqlite")
# .to_sql() создаст базу SQL для хранения датафрейма
# в указанной таблице. if_exists задает
# действие, которое нужно выполнить в том случае,
# если таблица уже существует
msft.to_sql("STOCK_DATA", connection, if_exists="replace")
aapl.to_sql("STOCK_DATA", connection, if_exists="append")
# подтверждаем отправку данных в базу и закрываем подключение
connection.commit()
connection.close()
# print("SQL Ok!")
# подключаемся к файлу базы данных
connection = sqlite3.connect(dir_dat+"stocks.sqlite")
# запрос всех записей в STOCK_DATA
# возвращает датафрейм
# index_col задает столбец, который нужно сделать
# индексом датафрейма
stocks = pd.io.sql.read_sql("SELECT * FROM STOCK_DATA;",
connection, index_col='index')
# закрываем подключение
connection.close()
# выводим первые 5 наблюдений в извлеченных данных
print(stocks[:5])
#
# открываем подключение
connection = sqlite3.connect(dir_dat+"stocks.sqlite")
# создаем строку-запрос
query = "SELECT * FROM STOCK_DATA WHERE " + \
    "Volume>29200100 AND Symbol='MSFT';"
# выполняем и закрываем подключение
items = pd.io.sql.read_sql(query, connection, index_col='index')
connection.close()
# выводим результат запроса
print(items)
# -------------------------------------------------    197
# импортируем пакет pandas_datareader
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as pdr
# считываем данные по GDP из FRED
gdp = pdr.data.FredReader("GDP",
date(2012, 1, 1),
date(2014, 1, 27))
print(gdp.read()[:5])
# получаем данные по показателю Compensation of employees:
# Wages and salaries
fr = pdr.data.FredReader("A576RC1A027NBEA",
date(1929, 1, 1),
date(2013, 1, 1)).read()[:5]
print(fr)
# считываем набор данных Global Factors из библиотеки Кеннета Френча
# factors = pdr.data.FamaFrenchReader("Global_Factors").read()   # 
# Empty DataFrame Columns: [Mkt-RF, SMB, HML, WML, RF]
# print(factors[0][:5])
# -------------------------------------------------    200
from pandas_datareader import wb
# извлекаем все индикаторы
all_indicators = pdr.wb.get_indicators()
# выводим первые 5 индикаторов
print(all_indicators.iloc[:5,:2])
# поиск индикаторов, связанных с продолжительностью жизни
le_indicators = pdr.wb.search("life expectancy")
# выводим первые три строки и первые два столбца
print(le_indicators.iloc[:5,:2])
# получаем список стран, показываем код и название
countries = pdr.wb.get_countries()
# выводим фрагмент списка стран
print(countries.loc[0:5,['name', 'capitalCity', 'iso2c']])
# получаем данные о продолжительности жизни
# для всех стран с 1980 по 2014 годы
le_data_all = pdr.wb.download(indicator="SP.DYN.LE00.IN",
start='1980',
end='2014')
print(le_data_all)




