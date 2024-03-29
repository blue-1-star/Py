import numpy as np 
import pandas as pd
from datetime import datetime
from datetime import timedelta
now = datetime.now()
print(now)
print(now.year, now.month, now.day)
delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
print(delta)
start = datetime(2011, 1, 7)
print(start + timedelta(12))
stamp = datetime(2011, 1, 3)
print(str(stamp))
print(stamp.strftime("%Y-%m-%d"))
print(stamp.strftime("%d-%m-%Y"))
value = "2011-01-03"
print(datetime.strptime(value, "%Y-%m-%d"))
datestrs = ["7/6/2011", "8/6/2011"]
print([datetime.strptime(x, "%m/%d/%Y") for x in datestrs])
print(pd.to_datetime(datestrs))
# p 357
dates = [datetime(2011, 1, 2), datetime(2011, 1, 5),
datetime(2011, 1, 7), datetime(2011, 1, 8),
datetime(2011, 1, 10), datetime(2011, 1, 12)]
ts = pd.Series(np.random.standard_normal(6), index=dates)
print(ts)
print(ts.index)
stamp = ts.index[2]
print(ts[stamp])
print(ts + ts[::2])








