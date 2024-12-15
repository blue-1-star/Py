from astropy.coordinates import get_body             # get_moon
from astropy.time import Time
from astropy.coordinates import GCRS,  EarthLocation, solar_system_ephemeris
import astropy.units as u
from astropy.utils.data import download_file

# Скачиваем данные эфемерид
# url = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp"
# url = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de431.bsp"
# local_path = download_file(url, cache=True)
# print("Файл загружен в:", local_path)

solar_system_ephemeris.set("de430");
# solar_system_ephemeris.set("de431")
# solar_system_ephemeris.set("builtin")
t0 = Time("2021-10-08T12:00")

loc = EarthLocation(lat=52*u.deg, lon=6*u.deg)
moon = get_body('moon', t0, loc)

res1 = moon.distance
# 361084.21km
print(f"res1: {res1.to(u.km)}")
# res2 = (moon(t0).cartesian - loc.get_gcrs(t0).cartesian).norm()
#  moon.cartesian: Получаем координаты Луны в декартовой системе (x, y, z).
#  loc.get_gcrs(t0).cartesian: Получаем координаты местоположения наблюдателя
#  в системе отсчёта GCRS (геоцентрическая инерциальная система отсчёта).
# .norm(): Расстояние между точками в декартовых координатах.
res2 = (moon.cartesian - loc.get_gcrs(t0).cartesian).norm()
# 361084.05km
print(f"res2: {res2.to(u.km)}")
r = res1.to(u.km) - res2.to(u.km)
print(f"res1 - res2: {r}")

print(r)
# res1 - res2
# 0.15716625km

