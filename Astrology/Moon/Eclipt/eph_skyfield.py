from skyfield.api import load

ts = load.timescale()
eph = load('de421.bsp')  # Эфемериды DE421 (или DE430)
moon = eph['moon']
earth = eph['earth']

t = ts.utc(2024, 11, 28, 0)  # Укажите дату и время
astrometric = earth.at(t).observe(moon).apparent()
ecliptic = astrometric.ecliptic_position()

print("Эклиптическая долгота:", ecliptic.longitude.degrees)
print("Эклиптическая широта:", ecliptic.latitude.degrees)
