import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from spor_calc_2 import process_fungus_stats, set_size
def bootstrap_statistic(data, statistic_func, n_iterations=1000):
    """
    Выполняет бутстреп для заданной статистики.
    
    Параметры:
    - data: Series или одномерный массив данных.
    - statistic_func: Функция, вычисляющая статистику для выборки.
    - n_iterations: Количество бутстреп-итераций.
    
    Возвращает массив значений статистики, вычисленных по бутстреп-выборкам.
    """
    boot_stats = []
    for _ in range(n_iterations):
        # Создаем бутстреп-выборку (случайная выборка с возвращением)
        boot_sample = data.sample(frac=1, replace=True)
        stat = statistic_func(boot_sample)
        boot_stats.append(stat)
    return np.array(boot_stats)

# Функция для вычисления среднего значения
def mean_statistic(data):
    return data.mean()

# Функция для вычисления положения максимума плотности (KDE-мода)
def kde_mode_statistic(data, xgrid=np.linspace(0, 200, 1000)):
    kde = gaussian_kde(data)
    y = kde(xgrid)
    return xgrid[np.argmax(y)]

# Пример использования для двух групп (например, worst и best)
# Предположим, что в merged_data есть столбцы 'BaseName' и 'Diameter'

data_xy_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\result.xlsx"
data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"
# Директория с изображениями
dir_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x"
    
_, merged_data = process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048)

worst_group = merged_data[merged_data['BaseName'].str.contains("worst", case=False, na=False)]['Diameter']
best_group = merged_data[merged_data['BaseName'].str.contains("best", case=False, na=False)]['Diameter']

# Бутстреп для среднего значения
boot_means_worst = bootstrap_statistic(worst_group, mean_statistic, n_iterations=1000)
boot_means_best = bootstrap_statistic(best_group, mean_statistic, n_iterations=1000)

# Бутстреп для KDE-моды (пика плотности)
boot_modes_worst = bootstrap_statistic(worst_group, lambda d: kde_mode_statistic(d), n_iterations=1000)
boot_modes_best = bootstrap_statistic(best_group, lambda d: kde_mode_statistic(d), n_iterations=1000)

# Вычисляем среднее и 95% доверительный интервал для каждой статистики
mean_worst = np.mean(boot_means_worst)
ci_mean_worst = np.percentile(boot_means_worst, [2.5, 97.5])
mean_best = np.mean(boot_means_best)
ci_mean_best = np.percentile(boot_means_best, [2.5, 97.5])

mode_worst = np.mean(boot_modes_worst)
ci_mode_worst = np.percentile(boot_modes_worst, [2.5, 97.5])
mode_best = np.mean(boot_modes_best)
ci_mode_best = np.percentile(boot_modes_best, [2.5, 97.5])



print("Worst group (FL12):")
print(f"  Mean diameter: {mean_worst:.2f} (95% CI: {ci_mean_worst[0]:.2f} - {ci_mean_worst[1]:.2f})")
print(f"  KDE mode: {mode_worst:.2f} (95% CI: {ci_mode_worst[0]:.2f} - {ci_mode_worst[1]:.2f})")

print("Best group (FL9):")
print(f"  Mean diameter: {mean_best:.2f} (95% CI: {ci_mean_best[0]:.2f} - {ci_mean_best[1]:.2f})")
print(f"  KDE mode: {mode_best:.2f} (95% CI: {ci_mode_best[0]:.2f} - {ci_mode_best[1]:.2f})")

