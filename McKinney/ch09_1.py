import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
data = np.arange(10)
print(data)
# plt.plot(data)
# plt.show()
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax3.plot(np.random.standard_normal(50).cumsum(), color="black",
linestyle="dashed")
ax1.hist(np.random.standard_normal(100), bins=20, color="black", alpha=0.3);
ax2.scatter(np.arange(30), np.arange(30) + 3 * np.random.standard_normal(30));
# plt.show()
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i, j].hist(np.random.standard_normal(500), bins=50,
        color="black", alpha=0.5)
fig.subplots_adjust(wspace=0, hspace=0)
# ax.plot(x, y, linestyle="--", color="green")
ax = fig.add_subplot()
ax.plot(np.random.standard_normal(30).cumsum(), color="black",
linestyle="dashed", marker="o");
fig = plt.figure()
ax = fig.add_subplot()
data = np.random.standard_normal(30).cumsum()
ax.plot(data, color="black", linestyle="dashed", label="Default");
# plt.show()
ax.plot(data, color="black", linestyle="dashed",
drawstyle="steps-post", label="steps-post");
ax.legend()
# pic 9.8
fig, ax = plt.subplots()
ax.plot(np.random.standard_normal(1000).cumsum());
ticks = ax.set_xticks([0, 250, 500, 750, 1000])
labels = ax.set_xticklabels(["one", "two", "three", "four", "five"],
rotation=30, fontsize=8)
ax.set_xlabel("Stages")
# Text(0.5, 6.666666666666652, 'Stages')
ax.set_title("My first matplotlib plot")
plt.show()

