import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

def plot_r2_comparison(y_true, y_pred, title="R² Comparison"):
    """
    Вычисляет R² и строит график сравнения истинных и предсказанных значений.
    
    Параметры:
    - y_true: массив, истинные (эталонные) значения.
    - y_pred: массив, предсказанные (измеренные) значения.
    - title: заголовок графика (по умолчанию "R² Comparison").
    
    Возвращает:
    - R² score (коэффициент детерминации).
    - График с линией идеального соответствия.
    """
    # Вычисляем R²
    r2 = r2_score(y_true, y_pred)
    
    # Строим график
    plt.figure(figsize=(8, 6))
    plt.scatter(y_true, y_pred, alpha=0.5, label=f"R² = {r2:.3f}")
    
    # Линия идеального соответствия (y_true = y_pred)
    max_val = max(np.max(y_true), np.max(y_pred))
    min_val = min(np.min(y_true), np.min(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label="Ideal Fit")
    
    # Настройки графика
    plt.xlabel("True Values", fontsize=12)
    plt.ylabel("Predicted Values", fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    
    return r2