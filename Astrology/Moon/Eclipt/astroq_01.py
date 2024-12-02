# from astroquery.jplhorizons import Horizons

# # Используем ISO 8601 формат для времени
# obj = Horizons(id='301', location='500@0', epochs='2024-11-28 14:00:00')
# eph = obj.ephemerides()
# print(eph)


from astroquery.jplhorizons import Horizons
julian_date = 2460272.08333
# Запрос координат Луны для определённой даты
# obj = Horizons(id='301', location='500@0', epochs='2024-11-28 14:00:00')
obj = Horizons(id='301', location='500@0', epochs=[julian_date])

eph = obj.ephemerides(quantities='31')

# Вывод результатов
print(eph['datetime_str'][0])  # Дата
print(eph['ECL_LON'][0])  # Эклиптическая долгота
print(eph['ECL_LAT'][0])  # Эклиптическая широта
print(eph['delta'][0] * 149597870.7)  # Расстояние в км

