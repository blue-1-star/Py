from astroquery.jplhorizons import Horizons

# ID Луны и эпохи
obj = Horizons(id='301', location='500@0', epochs={'start': '2024-11-28', 'stop': '2024-11-28', 'step': '1d'})

# Получение эфемерид
eph = obj.ephemerides()
print(eph)
