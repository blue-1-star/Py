import cv2
import numpy as np
# Загрузка изображения
file_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x\A best_4x_1_scale.png"
img = cv2.imread(file_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Пороговая обработка (например, метод Отсу)
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Морфологические операции
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=2)

# Поиск контуров
# contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Предполагаемый диаметр спор (в тех же единицах, что и изображение)
expected_diameter = 80  # примерное значение
expected_perimeter = np.pi * expected_diameter
tolerance = 0.2  # допустимое отклонение (20%)

min_perimeter = expected_perimeter * (1 - tolerance)
max_perimeter = expected_perimeter * (1 + tolerance)



spore_diameters = []
filtered_contours = []
for cnt in contours:
    perimeter = cv2.arcLength(cnt, True)
    if min_perimeter <= perimeter <= max_perimeter:
        filtered_contours.append(cnt)
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
    diameter = 2 * radius
    spore_diameters.append(diameter)        

# Отображение отфильтрованных контуров:
output = cv2.cvtColor(morph, cv2.COLOR_GRAY2BGR)
cv2.namedWindow("Filtered Contours", cv2.WINDOW_NORMAL)
# Устанавливаем размер окна, например, 800x600 пикселей
cv2.resizeWindow("Filtered Contours", 800, 600)
cv2.drawContours(output, filtered_contours, -1, (0, 255, 0), 2)
cv2.imshow("Filtered Contours", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
spore_count = len(spore_diameters)
print("Найдено спор:", spore_count)
# print("Диаметры спор:", spore_diameters)
print("Диаметры спор:", ", ".join(f"{x:.0f}" for x in spore_diameters))
