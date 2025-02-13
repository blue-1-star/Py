# Выделим область чашки Петри и разделим её на квадраты
# Найдём границы чашки с помощью детекции кругов (метод Хафа)

# Применяем размытие для снижения шума
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Ищем круги методом Хафа
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                           param1=50, param2=30, minRadius=100, maxRadius=300)

# Если круги найдены, берём первый (предполагаем, что он соответствует чашке Петри)
if circles is not None:
    circles = np.uint16(np.around(circles))
    x, y, r = circles[0, 0]  # Координаты центра и радиус
else:
    x, y, r = gray.shape[1]//2, gray.shape[0]//2, min(gray.shape)//3  # Если круг не найден, берём центр

# Создаём маску для выделения области чашки
mask = np.zeros_like(gray, dtype=np.uint8)
cv2.circle(mask, (x, y), r, 255, -1)

# Применяем маску
masked_image = cv2.bitwise_and(binary, binary, mask=mask)

# Отобразим маску и вырезанный круг
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(mask, cmap='gray')
ax[0].set_title("Маска чашки Петри")
ax[0].axis("off")

ax[1].imshow(masked_image, cmap='gray')
ax[1].set_title("Выделенная чашка Петри")
ax[1].axis("off")

plt.show()
