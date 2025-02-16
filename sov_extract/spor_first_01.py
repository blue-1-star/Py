import cv2
import numpy as np
import matplotlib.pyplot as plt
# Загрузка изображения
file_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x\A best_4x_1_scale.png"
img = cv2.imread(file_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

plt.figure(figsize=(8, 6))
plt.imshow(blur, cmap="gray")
plt.title("Gaussian Blurred Image")
plt.axis("off")
plt.show()

# Пороговая обработка (например, метод Отсу)
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Морфологические операции
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=2)

# Поиск контуров
# contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Создаем копию исходного изображения для рисования контуров
img_contours = img.copy()


spore_diameters = []
min_area = 10  # порог по площади для исключения шума, подбирается эмпирически

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < min_area:
        continue  # пропускаем мелкие шумовые объекты
    # Вычисляем круговость, если требуется:
    perimeter = cv2.arcLength(cnt, True)
    circularity = 4 * np.pi * area / (perimeter**2) if perimeter > 0 else 0
    if circularity < 0.5:
        continue  # можно отсеять объекты, имеющие форму, далёкую от круглой

    # Оценка диаметра
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
    diameter = 2 * radius
    spore_diameters.append(diameter)

# Подсчет количества спор
spore_count = len(spore_diameters)
# Рисуем найденные контуры зеленым цветом (цвет можно изменить)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
# Устанавливаем размер окна, например, 800x600 пикселей
cv2.resizeWindow("Contours", 800, 600)
cv2.imshow("Contours", img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Найдено спор:", spore_count)
print("Диаметры спор:", spore_diameters)
