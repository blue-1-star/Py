import seaborn as sns
import matplotlib.pyplot as plt

# 10 случайных цветов из Seaborn
colors = sns.color_palette("husl", 10)

plt.figure(figsize=(10, 2))
for i, color in enumerate(colors):
    plt.fill_between([i, i+1], 0, 1, color=color)
plt.xlim(0, 10)
plt.axis("off")
plt.show()
