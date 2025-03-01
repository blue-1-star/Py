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

def process_images_in_directory(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.png'):
            image_path = os.path.join(directory, file_name)
            region_growing_fixed_seed(image_path)

def edit_existing_overlay(image_path):
    region_growing_fixed_seed(image_path, edit_mode=True)

def show_processed_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith('_overlay.png')]
    if not files:
        print("No processed files found.")
        return
    
    print("Processed files:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    
    choice = input("Enter the number of the file to edit: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(files):
            edit_existing_overlay(os.path.join(directory, files[choice].replace('_overlay.png', '.png')))
    except ValueError:
        print("Invalid choice.")

def list_files(directory):
    """Выводит список обработанных и необработанных файлов."""
    processed = []
    unprocessed = []
    
    for file in os.listdir(directory):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            base, ext = os.path.splitext(file)
            processed_filename = base + "_overlay.png"
            
            if processed_filename in os.listdir(directory):
                processed.append(processed_filename)
            else:
                unprocessed.append(file)
    
    print("\nФайлы в каталоге:")
    print("\nОбработанные:")
    for f in processed:
        print(f)
    print("\nНеобработанные:")
    for f in unprocessed:
        print(f)    
    return processed, unprocessed



# image_path = r"G:\My\sov\extract\Spores\original_img\grow_reg\A_best_4x_11.png"
def get_file_lists(directory):
    """Формирует списки оригинальных файлов и обработанных."""
    all_files = [f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    original_files = set()
    overlay_files = set()

    for file in all_files:
        base, ext = os.path.splitext(file)
        if base.endswith("_overlay"):
            overlay_files.add(file)  # Файл отметки обработки
        else:
            original_files.add(file)  # Оригинальные файлы
    
    # Определяем, какие оригиналы уже обработаны
    processed = {f for f in original_files if f"{os.path.splitext(f)[0]}_overlay.png" in overlay_files}
    unprocessed = original_files - processed  # Только те, у которых нет _overlay

    return sorted(list(processed)), sorted(list(unprocessed))
	



def get_next_file(unprocessed, processed):
    """Ожидает выбора пользователя: обработка нового файла или редактирование."""
    while True:
        print("\nФайлы в каталоге:\n")
        print("Обработанные:")
        for f in processed:
            print(f"- {f}")

        print("\nНеобработанные:")
        for f in unprocessed:
            print(f"- {f}")

        print("\nНажмите Enter (или Space) для обработки следующего файла.")
        print("Введите 'edit' для выбора уже обработанного файла.")
        key = input("Ваш выбор: ").strip().lower()

        if key == "":  # Enter / Space -> берем следующий необработанный
            if unprocessed:
                return unprocessed.pop(0), False  # Новый файл, edit_mode=False
            else:
                print("Нет необработанных файлов.")
                continue  # Возвращаемся в цикл, не завершая функцию

        elif key == "edit":
            if not processed:
                print("Нет обработанных файлов для редактирования.")
                continue  # Возвращаемся в цикл, не завершая функцию

            print("Выберите номер обработанного файла для редактирования:")
            for idx, file in enumerate(processed, start=1):
                print(f"{idx}: {file}")

            try:
                choice = int(input("Введите номер: "))
                if 0 < choice <= len(processed):
                    selected_file = processed[choice - 1]
                    print(f"\nРедактируем: {selected_file}")
                    return selected_file, True  # Передаём файл и флаг edit_mode=True
                else:
                    print("Неверный номер. Попробуйте снова.")
                    continue  # Возвращаемся в цикл, не завершая функцию
            except ValueError:
                print("Ошибка ввода. Введите номер файла.")
                continue  # Возвращаемся в цикл, не завершая функцию

        # Если ввод не соответствует ни одному условию — продолжаем спрашивать пользователя
        print("Неверный ввод. Попробуйте снова.")
        continue  # Возвращаемся в начало цикла


if __name__ == "__main__":
    directory = r"G:\My\sov\extract\Spores\original_img\grow_reg"  # Укажите вашу папку
    processed, unprocessed = get_file_lists(directory)
    next_file, edit_mode = get_next_file(unprocessed, processed)

    if next_file:
        full_path = os.path.join(directory, next_file)  # Добавляем полный путь
        region_growing_fixed_seed(full_path, edit_mode=edit_mode)
        print(f"\nОбрабатываем: {next_file}")
        # region_growing_fixed_seed(next_file, edit_mode=edit_mode)
    else:
        print("\nНет доступных файлов для обработки.")

