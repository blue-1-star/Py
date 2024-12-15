"""
https://github.com/egemenimre/satstuff/blob/master/notebooks/astropy/moon_venus_phase.ipynb

Compute Moon and Venus Phase Angles with astropy

As an addition to the Sun and Moon Altitudes and Sun Rise Set times, this notebook shows the steps
to compute the Phase Angles for Moon and Venus.
Phase Angle defines the angle between the Sun, the Observed Object (e.g. Moon) and the Observer (you).
Phase angle 0 for Moon corresponds to Full Moon (though actually you see a value close to, but not exactly equal to 0 degrees)
and 180 deg corresponds to New Moon.
The initial configuration of time and locations are similar to the Sun and Moon Altitudes, so I will not go into detailed explanations. This time, though, the simulation duration is much longer and stepsizes are much larger, as the motion of the Moon is slow and that of Venus is even slower.
"""



from astropy.coordinates import EarthLocation
from astropy import units as u
from astropy.time import Time, TimeDelta

import pytz

# Init location - default Ellipsoid is WGS84
istanbul: EarthLocation = EarthLocation(lat=41.015137, lon=28.979530, height=0 * u.m)
ist_timezone = pytz.timezone("Turkey")
utc_timezone = pytz.timezone("utc")
print(f"Target coordinates (lat,lon): {istanbul.lat}, {istanbul.lon}")

# Time analysis config (stepsize, duration, init time)
init_time: Time = Time("2020-04-01T00:00:00", scale="utc")
dt = TimeDelta(0.1, format="jd")  # stepsize
duration = TimeDelta(90.0, format="jd")  # duration

"""
The next step is to set up the time steps and initialise the Sun, Moon and Venus vectors in Geocentric Celestial Reference System (GCRS)
i.e., an inertially fixed coordinate system with its centre at the Earth. This frame is fixed (not rotating) with respect to the stars.
It is also what people usually mean when people talk about the Earth Centred Inertial coordinate system.
We also use these results in Cartesian form as they yield themselves well to the vector operations we will make later.
"""
import numpy as np
from astropy.coordinates import get_moon, get_sun, get_body, SkyCoord

# Generate observation time list
dt_list = dt * np.arange(0, duration.sec / dt.sec, 1)
obs_times: Time = init_time + dt_list

# Generate Sun, Moon and Venus coordinates
sun_vec_gcrs: SkyCoord = get_sun(obs_times).cartesian
moon_vec_gcrs: SkyCoord = get_moon(obs_times).cartesian
venus_vec_gcrs: SkyCoord = get_body("venus", obs_times).cartesian

# Generate Earth location in GCRS
gnd_loc_gcrs = istanbul.get_gcrs(obs_times).cartesian.without_differentials()

# 
from astropy.coordinates import CartesianRepresentation

# Generate Sun, Moon and Venus-to-Istanbul vectors
sun_to_moon: CartesianRepresentation = sun_vec_gcrs - moon_vec_gcrs
gnd_to_moon: CartesianRepresentation = gnd_loc_gcrs - moon_vec_gcrs

sun_to_venus: CartesianRepresentation = sun_vec_gcrs - venus_vec_gcrs
gnd_to_venus: CartesianRepresentation = gnd_loc_gcrs - venus_vec_gcrs

# Compute angle between two vectors for each instant in time
sun_to_moon_unit = sun_to_moon / sun_to_moon.norm()
gnd_to_moon_unit = gnd_to_moon / gnd_to_moon.norm()
phase_angle_moon = np.rad2deg(np.arccos(sun_to_moon_unit.dot(gnd_to_moon_unit)))

sun_to_venus_unit = sun_to_venus / sun_to_venus.norm()
gnd_to_venus_unit = gnd_to_venus / gnd_to_venus.norm()
phase_angle_venus = np.rad2deg(np.arccos(sun_to_venus_unit.dot(gnd_to_venus_unit)))

print(f"Moon phase angle  : {phase_angle_moon[0]} at {obs_times[0].to_datetime(timezone=utc_timezone)}")
print(f"Venus phase angle : {phase_angle_venus[0]} at {obs_times[0].to_datetime(timezone=utc_timezone)}")

# Moon phase angle  : 95.59782267821191 deg at 2020-04-01 00:00:00+00:00
# Venus phase angle : 93.30428615880972 deg at 2020-04-01 00:00:00+00:00
# 