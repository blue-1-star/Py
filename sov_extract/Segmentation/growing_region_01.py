import cv2
import numpy as np

def region_growing_fixed_seed(img, seed, thresh, display_interval=100):
    """
    Алгоритм регионального роста с сравнением каждого пикселя с исходным значением seed.
    
    Параметры:
      img             - изображение в оттенках серого.
      seed            - координаты начальной точки (x, y).
      thresh          - порог допускаемой разницы интенсивности.
      display_interval- количество итераций между обновлением экрана.
      
    Возвращает:
      mask - бинарная маска выделенного региона.
    """
    h, w = img.shape
    mask = np.zeros((h, w), np.uint8)
    seed_value = int(img[seed[1], seed[0]])
    seed_list = [seed]
    mask[seed[1], seed[0]] = 255
    iteration = 0

    while seed_list:
        x, y = seed_list.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                    # Сравниваем новый пиксель с исходным значением seed
                    if abs(int(img[ny, nx]) - seed_value) < thresh:
                        mask[ny, nx] = 255
                        seed_list.append((nx, ny))
        iteration += 1
        if iteration % display_interval == 0:
            cv2.imshow("Процесс регионального роста", mask)
            cv2.waitKey(1)
    return mask

# Загрузка исходного изображения
image_path = r"G:\My\sov\extract\Spores\original_img\worst\test\A_best_4x_11.png"  # Замените на путь к вашему файлу с микроскопическим изображением
img_color = cv2.imread(image_path)
if img_color is None:
    print("Ошибка загрузки изображения!")
    exit()

# Преобразование изображения в оттенки серого
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Функция обработки клика мыши
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x, y)
        print("Выбрана seed точка:", seed)
        seg_mask = region_growing_fixed_seed(img_gray, seed, thresh=15, display_interval=200)
        cv2.imshow("Финальная маска", seg_mask)
        overlay = img_color.copy()
        overlay[seg_mask==255] = (0, 0, 255)
        cv2.imshow("Наложение маски", overlay)

# Создаем окно с возможностью изменения размера
window_name = "Выберите seed точку"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 800, 600)  # Задайте размеры, удобные для вашего экрана
cv2.imshow(window_name, img_color)
cv2.setMouseCallback(window_name, click_event)

print("Щёлкните левой кнопкой мыши по споре для запуска алгоритма регионального роста.")
cv2.waitKey(0)
cv2.destroyAllWindows()
