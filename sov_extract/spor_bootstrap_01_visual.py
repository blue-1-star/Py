import matplotlib.pyplot as plt
import numpy as np
import os
# Результаты для группы FL12 (Worst)
mean_FL12 = 53.03
mean_FL12_lower = 53.03 - 49.45  # разница между оценкой и нижней границей
mean_FL12_upper = 57.60 - 53.03  # разница между верхней границей и оценкой

mode_FL12 = 33.44
mode_FL12_lower = 33.44 - 29.03
mode_FL12_upper = 38.84 - 33.44

# Результаты для группы FL9 (Best)
mean_FL9 = 38.49
mean_FL9_lower = 38.49 - 36.75
mean_FL9_upper = 40.18 - 38.49

mode_FL9 = 32.68
mode_FL9_lower = 32.68 - 28.02
mode_FL9_upper = 36.04 - 32.68


data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"
graph_dir = os.path.join(os.path.dirname(data_scale_path), "graph")


# Список групп
groups = ['FL12', 'FL9']

# Данные для среднего диаметра
means = [mean_FL12, mean_FL9]
mean_errors = [[mean_FL12_lower, mean_FL9_lower],
               [mean_FL12_upper, mean_FL9_upper]]

# Данные для моды (KDE mode)
modes = [mode_FL12, mode_FL9]
mode_errors = [[mode_FL12_lower, mode_FL9_lower],
               [mode_FL12_upper, mode_FL9_upper]]

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# График для среднего диаметра
# axs[0].bar(groups, means, color=['skyblue', 'lightgreen'], alpha=0.8, zorder=2)
axs[0].bar(groups, means, color=['skyblue', 'lightgreen'], alpha=0.8, zorder=2)
axs[0].errorbar(groups, means, yerr=mean_errors, fmt='none', color='black', capsize=5, zorder=3)
axs[0].set_title('Mean Sporangium Diameter')
axs[0].set_ylabel('Sporangium Diameter (μm)')
axs[0].grid(axis='y', linestyle='--', alpha=0.7)

# График для моды (KDE mode)
# axs[1].bar(groups, modes, color=['skyblue', 'lightgreen'], alpha=0.8, zorder=2)
axs[1].bar(groups, modes, color=['skyblue', 'lightgreen'], alpha=0.8, zorder=2)
axs[1].errorbar(groups, modes, yerr=mode_errors, fmt='none', color='black', capsize=5, zorder=3)
axs[1].set_title('KDE Mode of Sporangium Diameter')
axs[1].set_ylabel('Sporangium Diameter (μm)')
axs[1].grid(axis='y', linestyle='--', alpha=0.7)

plt.suptitle('Comparison of Sporangium Diameter Statistics between Groups', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
boots_chart_path = os.path.join(graph_dir, "boots_chart.png")
plt.savefig(boots_chart_path, bbox_inches='tight')
plt.show()
