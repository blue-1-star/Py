from astroquery.jplhorizons import Horizons

def get_lunar_coordinates(time):
    """Получает эклиптические координаты Луны из NASA Horizons."""
    obj = Horizons(id='301',  # Идентификатор Луны
                   location='500@0',  # Центр Земли
                   epochs=time)  # Время в формате JD или ISO
    eph = obj.ephemerides()
    return {
        "longitude": eph['ECL_LON'][0],  # Эклиптическая долгота
        "latitude": eph['ECL_LAT'][0],   # Эклиптическая широта
        "distance": eph['delta'][0] * 149597870.7,  # Расстояние в км
    }

# Пример использования:
time = "2024-11-28 14:00"
result = get_lunar_coordinates(time)
print(f"Долгота: {result['longitude']}°, Широта: {result['latitude']}°, Расстояние: {result['distance']} км")
