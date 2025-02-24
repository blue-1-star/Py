import cv2
import numpy as np

def region_growing(img, seed, thresh, display_interval=100):
    """
    Алгоритм регионального роста с периодическим обновлением отображения процесса.
    
    Параметры:
      img             - изображение в оттенках серого.
      seed            - координаты начальной точки (x, y).
      thresh          - порог допускаемой разницы интенсивности.
      display_interval- количество итераций между обновлениями экрана.
      
    Возвращает:
      mask - бинарная маска выделенного региона.
    """
    h, w = img.shape
    mask = np.zeros((h, w), np.uint8)
    seed_list = [seed]
    mask[seed[1], seed[0]] = 255

    iteration = 0
    while seed_list:
        x, y = seed_list.pop(0)
        # Проходим по 8-соседям
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                    # Добавляем пиксель, если разница интенсивности меньше порога
                    if abs(int(img[ny, nx]) - int(img[y, x])) < thresh:
                        mask[ny, nx] = 255
                        seed_list.append((nx, ny))
        iteration += 1
        # Обновляем изображение процесса каждые display_interval итераций
        if iteration % display_interval == 0:
            cv2.imshow("Процесс регионального роста", mask)
            cv2.waitKey(1)  # небольшой промежуток для обновления окна
    return mask

# Загрузка исходного изображения
image_path = r"G:\My\sov\extract\Spores\original_img\worst\test\A_best_4x_11.png"  # Замените на путь к вашему файлу с микроскопическим изображением
# image_path = "path_to_your_image.jpg"  # Замените на путь к вашему изображению
img_color = cv2.imread(image_path)
if img_color is None:
    print("Ошибка загрузки изображения!")
    exit()

# Преобразуем изображение в оттенки серого
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Функция для выбора seed точки (обработка клика мыши)
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x, y)
        print("Выбрана seed точка:", seed)
        # Можно экспериментировать с порогом – например, 10, 15 или другой, в зависимости от качества изображения
        seg_mask = region_growing(img_gray, seed, thresh=10, display_interval=200)
        cv2.imshow("Финальная маска", seg_mask)
        # Отображение наложения маски на оригинальное изображение для визуальной проверки
        overlay = img_color.copy()
        overlay[seg_mask==255] = (0, 0, 255)
        cv2.imshow("Наложение маски", overlay)

# Создаем окно для выбора seed точки
cv2.namedWindow("Выберите seed точку", cv2.WINDOW_NORMAL)
cv2.imshow("Выберите seed точку", img_color)
cv2.setMouseCallback("Выберите seed точку", click_event)

print("Щёлкните левой кнопкой мыши по споре для запуска алгоритма регионального роста.")
cv2.waitKey(0)
cv2.destroyAllWindows()
