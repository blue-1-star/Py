# p 296
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from datetime import datetime
fig, ax = plt.subplots()
data = pd.read_csv("McKinney/examples/spx.csv", index_col=0, parse_dates=True)
# print(data)
spx = data["SPX"]
spx.plot(ax=ax, color="black")
crisis_data = [
(datetime(2007, 10, 11), "Peak of bull market"),
(datetime(2008, 3, 12), "Bear Stearns Fails"),
(datetime(2008, 9, 15), "Lehman Bankruptcy")
]
for date, label in crisis_data:
    ax.annotate(label, xy=(date, spx.asof(date) + 75),
    xytext=(date, spx.asof(date) + 225),
    arrowprops=dict(facecolor="black", headwidth=4, width=2,
    headlength=4),
    horizontalalignment="left", verticalalignment="top")
ax.set_xlim(["1/1/2007", "1/1/2011"])
ax.set_ylim([600, 1800])
ax.set_title("Important dates in the 2008-2009 financial crisis")
# 
fig, ax = plt.subplots()
rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color="black", alpha=0.3)
circ = plt.Circle((0.7, 0.2), 0.15, color="blue", alpha=0.3)
pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]],
color="green", alpha=0.5)
ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)
plt.show()
s = pd.Series(np.random.standard_normal(10).cumsum(), index=np.arange(0,
100, 10))
s.plot()
plt.show()

