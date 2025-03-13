import os
import cv2
import numpy as np
import pandas as pd

def region_growing_fixed_seed(image_path, threshold=15, base_mode='seed', edit_mode=False):
    """
    Запускает процесс сегментации изображения.
    В режиме редактирования (edit_mode=True) работает с уже обработанным файлом.
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
    
    def find_nearest_seed(click_x, click_y):
        min_distance = float('inf')
        nearest_index = None
        
        for i, entry in enumerate(region_data):
            seed_x, seed_y = entry[2], entry[3]
            distance = ((seed_x - click_x) ** 2 + (seed_y - click_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_index = i
        
        return nearest_index if min_distance < 20 else None  # Пороговое расстояние 20 пикселей
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal seed
        if event == cv2.EVENT_LBUTTONDOWN:
            seed = (y, x)
        elif event == cv2.EVENT_RBUTTONDOWN and edit_mode:  # Правая кнопка для удаления
            index = find_nearest_seed(y, x)
            if index is not None:
                removed_seed = region_data.pop(index)
                overlay[:] = image.copy()  # Перерисовываем заново
                for entry in region_data:
                    mask, _ = region_growing((entry[2], entry[3]))
                    overlay[mask == 255] = (0, 255, 0)
                print(f"Removed seed: {removed_seed}")
    
    cv2.namedWindow(file_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(file_name, 1980, 1320)
    cv2.setMouseCallback(file_name, mouse_callback)
    
    def region_growing(seed):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        queue = [seed]
        seed_value = image[seed[0], seed[1]].mean()
        iteration_count = 0
        
        while queue:
            x, y = queue.pop()
            if mask[x, y] == 0 and abs(int(image[x, y].mean()) - int(seed_value)) < threshold:
                mask[x, y] = 255
                overlay[x, y] = (0, 255, 0)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < image.shape[0] and 0 <= ny < image.shape[1]:
                        queue.append((nx, ny))
                iteration_count += 1
        
        return mask, iteration_count


    while True:
        cv2.imshow(file_name, overlay)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('n'):
            break
        if key == 27:  # ESC
            print("Exiting program")
            break
        
        if (key == ord(' ') or key == 13) and seed is not None:  # Добавление новой seed-точки
            mask, iterations = region_growing(seed)
            region_area = np.sum(mask == 255)
            seed_rgb = image[seed[0], seed[1]].tolist()
            
            region_data.append([file_name, spore_count, seed[0], seed[1], iterations, seed_rgb, region_area, threshold, base_mode])
            spore_count += 1
            
            overlay[mask == 255] = (0, 255, 0)
            seed = None  # Сбрасываем seed после обработки
    
    cv2.destroyAllWindows()
    
    cv2.imwrite(overlay_path, overlay)
    print(f"Overlay saved at: {overlay_path}")
    
    df = pd.DataFrame(region_data, columns=["Filename", "Spore Number", "Seed X", "Seed Y", "Iterations", "RGB", "Region Area", "Threshold", "Base Mode"])
    df.to_excel(auto_select_path, index=False)
    print(f"Updated auto_select_region saved at: {auto_select_path}")

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

# def list_files(directory):
#     """Выводит список обработанных и необработанных файлов."""
#     processed = []
#     unprocessed = []
    
#     for file in os.listdir(directory):
#         if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
#             base, ext = os.path.splitext(file)
#             processed_filename = base + "_overlay.png"
            
#             if processed_filename in os.listdir(directory):
#                 processed.append(processed_filename)
#             else:
#                 unprocessed.append(file)
    
#     print("\nФайлы в каталоге:")
#     print("\nОбработанные:")
#     for f in processed:
#         print(f)
#     print("\nНеобработанные:")
#     for f in unprocessed:
#         print(f)    
#     return processed, unprocessed



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



