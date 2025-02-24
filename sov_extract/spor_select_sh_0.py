import cv2
import pandas as pd
import os
from PIL import Image  # если требуется обработка изображений

def select_shapes(image_path, mode='rectangle'):
    """
    Функция загружает изображение, позволяет интерактивно выбрать фигуры 
    (точки, прямоугольники или эллипсы) и возвращает DataFrame с результатами.
    На изображении выбранные фигуры нумеруются.
    Результирующее изображение сохраняется в том же каталоге с суффиксом _cont_sel.png.
    
    Параметры:
      image_path  - полный путь к изображению.
      mode        - режим выбора: 'point', 'rectangle' или 'ellipse'.
    
    Возвращает:
      DataFrame с данными (если выбраны фигуры) или None.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Ошибка: не удалось загрузить изображение {image_path}!")
        return None

    # Создаем окно с возможностью изменения размера
    window_name = "Image"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(window_name, 800, 600)  # Можно изменить начальный размер окна
    cv2.resizeWindow(window_name, 1980, 1320)  # Можно изменить начальный размер окна

    # Копия для отрисовки
    clone = img.copy()
    
    shape_index = 0      # Счётчик фигур
    shapes = []          # Список для хранения результатов выбранных фигур
    current_click = []   # Для хранения кликов, когда фигура определяется более чем одной точкой
    
    def click_event(event, x, y, flags, param):
        nonlocal img, shape_index, shapes, current_click
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode == 'point':
                shape_index += 1
                shapes.append({'index': shape_index, 'x': x, 'y': y})
                # Рисуем точку и номер
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(img, str(shape_index), (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif mode == 'rectangle':
                current_click.append((x, y))
                if len(current_click) == 1:
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(current_click) == 2:
                    shape_index += 1
                    pt1, pt2 = current_click[0], current_click[1]
                    shapes.append({'index': shape_index, 'pt1': pt1, 'pt2': pt2})
                    cv2.rectangle(img, pt1, pt2, (255, 0, 0), 2)
                    # Выбираем позицию для подписи – в верхнем левом углу прямоугольника
                    label_x = min(pt1[0], pt2[0])
                    label_y = min(pt1[1], pt2[1])
                    cv2.putText(img, str(shape_index), (label_x + 5, label_y + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_click.clear()
            elif mode == 'ellipse':
                current_click.append((x, y))
                if len(current_click) == 1:
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(current_click) == 2:
                    shape_index += 1
                    pt1, pt2 = current_click[0], current_click[1]
                    center_x = int((pt1[0] + pt2[0]) / 2)
                    center_y = int((pt1[1] + pt2[1]) / 2)
                    axis_x = abs(pt2[0] - pt1[0]) // 2
                    axis_y = abs(pt2[1] - pt1[1]) // 2
                    shapes.append({'index': shape_index, 'pt1': pt1, 'pt2': pt2,
                                   'center': (center_x, center_y), 'axes': (axis_x, axis_y)})
                    cv2.ellipse(img, (center_x, center_y), (axis_x, axis_y), 0, 0, 360, (0, 255, 255), 2)
                    cv2.putText(img, str(shape_index), (center_x - 10, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_click.clear()
            cv2.imshow(window_name, img)

    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, click_event)
    print("Левая кнопка мыши для выбора фигур.")
    print("Нажмите ESC для завершения выбора (окно с изображением должно быть активным).")

    # Ждем, пока пользователь не нажмет ESC
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            if mode in ['rectangle', 'ellipse'] and current_click:
                print("Незавершённая фигура отброшена.")
                current_click.clear()
            break
    cv2.destroyAllWindows()

    # Сохраняем финальное изображение с нанесёнными фигурами
    base, ext = os.path.splitext(image_path)
    output_image_path = base + "_cont_sel.png"
    cv2.imwrite(output_image_path, img)
    print(f"Изображение с выбранными фигурами сохранено: {output_image_path}")

    # Формирование данных для сохранения в Excel
    if mode == 'point':
        if not shapes:
            print("Нет выбранных точек.")
            return None
        data = {"Index": [], "Image": [], "X": [], "Y": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(os.path.basename(image_path))
            data["X"].append(s['x'])
            data["Y"].append(s['y'])
    elif mode == 'rectangle':
        if not shapes:
            print("Нет выбранных прямоугольников.")
            return None
        data = {"Index": [], "Image": [], "X1": [], "Y1": [], "X2": [], "Y2": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(os.path.basename(image_path))
            data["X1"].append(s['pt1'][0])
            data["Y1"].append(s['pt1'][1])
            data["X2"].append(s['pt2'][0])
            data["Y2"].append(s['pt2'][1])
    elif mode == 'ellipse':
        if not shapes:
            print("Нет выбранных эллипсов.")
            return None
        data = {"Index": [], "Image": [],
                "CenterX": [], "CenterY": [],
                "AxisX": [], "AxisY": [],
                "Pt1X": [], "Pt1Y": [],
                "Pt2X": [], "Pt2Y": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(os.path.basename(image_path))
            data["CenterX"].append(s['center'][0])
            data["CenterY"].append(s['center'][1])
            data["AxisX"].append(s['axes'][0])
            data["AxisY"].append(s['axes'][1])
            data["Pt1X"].append(s['pt1'][0])
            data["Pt1Y"].append(s['pt1'][1])
            data["Pt2X"].append(s['pt2'][0])
            data["Pt2Y"].append(s['pt2'][1])
    df = pd.DataFrame(data)
    return df

def process_directory(directory, mode='rectangle', excel_file='results.xlsx'):
    """
    Обходит все файлы в каталоге, для каждого файла, который еще не обработан
    (если имя файла не заканчивается на _cont_sel.png и отсутствует файл с таким суффиксом),
    вызывается функция select_shapes. Результаты для всех файлов накапливаются и добавляются
    в Excel-файл. При сохранении в Excel в столбце "Image" указывается только базовое имя файла.
    
    Параметры:
      directory   - каталог с изображениями.
      mode        - режим выбора: 'point', 'rectangle' или 'ellipse'.
      excel_file  - Excel-файл, в который будут добавляться результаты.
    """
    # Если Excel-файл уже существует, загружаем его, иначе создаем пустой DataFrame
    if os.path.exists(excel_file):
        combined_df = pd.read_excel(excel_file)
    else:
        combined_df = None

    # Перебираем файлы в каталоге
    for file in os.listdir(directory):
        # Пропускаем файлы, имя которых уже содержит суффикс _cont_sel.png
        if file.lower().endswith('_cont_sel.png'):
            print(f"Файл {file} уже обработан, пропускаем.")
            continue

        # Обрабатываем только файлы с нужными расширениями
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            base, ext = os.path.splitext(file)
            processed_filename = base + "_cont_sel.png"
            processed_filepath = os.path.join(directory, processed_filename)
            
            # Если обработанный файл уже существует, пропускаем текущий файл
            if os.path.exists(processed_filepath):
                print(f"Файл {file} уже обработан, пропускаем.")
                continue

            image_path = os.path.join(directory, file)
            print(f"\nОбработка файла: {image_path}")
            result_df = select_shapes(image_path, mode=mode)
            if result_df is not None and not result_df.empty:
                if combined_df is None:
                    combined_df = result_df
                else:
                    combined_df = pd.concat([combined_df, result_df], ignore_index=True)
            else:
                print(f"Файл {file}: нет данных для сохранения.")

    if combined_df is not None:
        try:
            combined_df.to_excel(excel_file, index=False)
            print(f"\nВсе результаты сохранены в файле {excel_file}")
        except Exception as e:
            print(f"Ошибка при сохранении файла {excel_file}: {e}")
            base_name, ext = os.path.splitext(excel_file)
            new_excel_file = base_name + "_1" + ext
            try:
                combined_df.to_excel(new_excel_file, index=False)
                print(f"\nВсе результаты сохранены в файле {new_excel_file}")
            except Exception as e2:
                print(f"Ошибка при сохранении в {new_excel_file}: {e2}")
    else:
        print("Нет данных для сохранения в Excel.")



if __name__ == "__main__":
    # Укажите путь к каталогу с изображениями
    directory = r"G:\My\sov\extract\Spores\original_img\test\best\4x"  # Замените на ваш путь
    # directory = r"G:\My\sov\extract\Spores\original_img\worst\test"  # Замените на ваш путь
    # Выберите режим: 'point', 'rectangle' или 'ellipse'
    excel_file = os.path.join(directory,"result.xlsx")
    process_directory(directory, mode='rectangle', excel_file=excel_file)
    # process_directory(directory, mode='ellipse', excel_file=excel_file)
