import os
import cv2
import pandas as pd
import numpy as np

def region_growing_fixed_seed(image_path, threshold=15, base_mode='seed', edit_mode=False):
    """
    Запускает процесс сегментации изображения.
    В режиме редактирования (edit_mode=True) работает с уже обработанным файлом.
    Позволяет отменять последний выбор точки (Ctrl+Z) в текущем сеансе.
    """
    mode_text = "Редактирование" if edit_mode else "Обычная обработка"
    print(f"\n{mode_text}: {image_path}")

    directory = os.path.dirname(image_path)
    graph_dir = directory  # Теперь overlay сохраняется в текущем каталоге
    
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return
    
    file_name = os.path.basename(image_path)
    overlay_path = os.path.join(graph_dir, file_name.replace('.png', '_overlay.png'))
    auto_select_path = os.path.join(directory, 'auto_select_region.xlsx')

    # Проверяем, был ли уже обработан файл
    if not edit_mode and os.path.exists(overlay_path):
        print(f"{file_name} уже обработан, пропускаем.")
        return

    # Загружаем или создаем overlay
    if os.path.exists(overlay_path):
        overlay = cv2.imread(overlay_path)
    else:
        overlay = image.copy()
    
    # Загружаем существующие данные из Excel, если они есть
    if os.path.exists(auto_select_path):
        df = pd.read_excel(auto_select_path)
    else:
        df = pd.DataFrame(columns=["Filename", "Spore Number", "Seed X", "Seed Y", "Iterations", "RGB", "Region Area", "Threshold", "Base Mode"])
    
    region_data = df.values.tolist()
    spore_count = len(region_data) + 1 if not edit_mode else max(df["Spore Number"].values, default=0) + 1

    seed = None
    seed_points = []  # Список выбранных пользователем точек

    window_name = f"Region Growing - {file_name}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    def find_nearest_seed(click_x, click_y):
        """Находит ближайшую уже выбранную точку (если режим редактирования)."""
        if not seed_points:
            return None
        return min(seed_points, key=lambda p: (p[0] - click_x) ** 2 + (p[1] - click_y) ** 2)

    def region_growing(seed):
        """Выполняет сегментацию от заданной точки."""
        nonlocal overlay
        if seed is None:
            return

        x, y = seed
        print(f"Выполняется region growing от точки: {x}, {y}")

        # Простейший алгоритм region growing (замените на свою логику)
        mask = np.zeros((image.shape[0] + 2, image.shape[1] + 2), np.uint8)
        connectivity = 4
        flags = connectivity | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
        cv2.floodFill(overlay, mask, (x, y), (0, 255, 0), loDiff=(threshold,)*3, upDiff=(threshold,)*3, flags=flags)

    def update_display():
        """Обновляет изображение с выделенными точками."""
        display_img = overlay.copy()
        for x, y in seed_points:
            cv2.circle(display_img, (x, y), 5, (0, 0, 255), -1)  # Отмечаем точки

        cv2.imshow(window_name, display_img)

    def mouse_callback(event, x, y, flags, param):
        """Обрабатывает нажатия мыши."""
        nonlocal seed
        if event == cv2.EVENT_LBUTTONDOWN:
            if edit_mode:
                seed = find_nearest_seed(x, y)  # В режиме редактирования ищем ближайшую точку
            else:
                seed = (x, y)  # Обычный режим — используем клик как seed

            if seed:
                seed_points.append(seed)  # Запоминаем точку
                print(f"Выбрана точка: {seed}")
                region_growing(seed)
                update_display()

    def keyboard_event():
        """Обрабатывает нажатие клавиш."""
        nonlocal overlay
        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # ESC - выйти
                break
            elif key == 26:  # Ctrl+Z - отмена последнего выбора
                if seed_points:
                    removed_point = seed_points.pop()  # Удаляем последнюю точку
                    print(f"Отменена точка: {removed_point}")
                    overlay = image.copy()  # Восстанавливаем оригинальное изображение
                    for point in seed_points:  # Пересчитываем оставшиеся точки
                        region_growing(point)
                    update_display()
                else:
                    print("Нет точек для отмены.")

    cv2.imshow(window_name, overlay)
    cv2.setMouseCallback(window_name, mouse_callback)
    print("Левая кнопка мыши - выбрать точку.")
    print("Ctrl+Z - отменить последний выбор.")
    print("ESC - завершить.")

    keyboard_event()  # Запускаем обработку клавиш
    cv2.destroyAllWindows()
