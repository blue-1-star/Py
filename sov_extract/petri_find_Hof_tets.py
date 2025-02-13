import cv2
import numpy as np

# Путь к изображению
image_path = r"G:\My\sov\extract\ORF\fungus\FL_1.jpg"

# Загружаем изображение
image = cv2.imread(image_path)
if image is None:
    print("Не удалось загрузить изображение по пути:", image_path)
    exit()

# width, height = image.size
height, width = image.shape[:2]
# Преобразуем изображение в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применяем гауссовское размытие для уменьшения шума
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Параметры для HoughCircles под ваш конкретный случай
# Если ожидается один большой круг, то:
# - Увеличиваем minDist, чтобы исключить пересечения
# - Повышаем порог param1 для оператора Canny и param2 для подтверждения центра
# - Устанавливаем диапазон радиусов так, чтобы отсеять мелкие круги
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,          # обратное отношение разрешений
    minDist=200,     # минимальное расстояние между центрами кругов (настраивайте по необходимости)
    param1=100,      # верхний порог для Canny (увеличен для уменьшения шума)
    param2=50,       # порог для обнаружения центра круга (увеличив его, можно отсеять слабые/ложные круги)
    minRadius=80,    # минимальный радиус (в пикселях); подбирайте согласно масштабу изображения
    maxRadius=150    # максимальный радиус (в пикселях)
)

# Фильтруем найденные круги (отбрасываем те, которые меньше ожидаемого размера)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    
    # Список для отфильтрованных кругов
    filtered_circles = []
    
    for (x, y, r) in circles:
        # Если круг слишком маленький, пропускаем его
        if r < 80:
            continue
        filtered_circles.append((x, y, r))
        # Рисуем внешний контур круга жирной зеленой линией (толщина 3 пикселя)
        cv2.circle(image, (x, y), r, (0, 255, 0), thickness=3)
        # Рисуем центр круга красным цветом (опционально)
        cv2.circle(image, (x, y), 2, (0, 0, 255), thickness=3)
    
    if not filtered_circles:
        print("После фильтрации по радиусу подходящих кругов не найдено.")
else:
    print("Круги не найдены.")

print(f'width = {width}, height={height}')
# Создаем окно с изменяемым размером и устанавливаем его размер (например, 600x600 пикселей)
cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Result", width//5, height//5)

# Отображаем результат
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
