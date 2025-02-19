import cv2
import pandas as pd

def select_shapes(image_path, mode='point', excel_file='results.xlsx'):
    """
    Функция загружает изображение, позволяет выбрать фигуры (точки, прямоугольники, эллипсы)
    с помощью мыши и сохраняет результаты (с порядковыми номерами) в Excel.
    
    Параметры:
      image_path  - путь к изображению.
      mode        - режим выбора: 'point', 'rectangle' или 'ellipse'.
      excel_file  - имя Excel-файла для сохранения результатов.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка: не удалось загрузить изображение!")
        return
    # Создаем копию изображения для отрисовки
    clone = img.copy()
    
    # Счетчик фигур
    shape_index = 0

    # Список для хранения результатов выбранных фигур
    shapes = []
    # Для хранения кликов, когда фигура определяется более чем одной точкой
    current_click = []
    
    def click_event(event, x, y, flags, param):
        nonlocal img, shape_index, shapes, current_click
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode == 'point':
                shape_index += 1
                shapes.append({'index': shape_index, 'x': x, 'y': y})
                # Рисуем точку и подписываем её номером
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(img, str(shape_index), (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif mode == 'rectangle':
                current_click.append((x, y))
                if len(current_click) == 1:
                    # Отмечаем первую точку
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(current_click) == 2:
                    shape_index += 1
                    pt1, pt2 = current_click[0], current_click[1]
                    shapes.append({'index': shape_index, 'pt1': pt1, 'pt2': pt2})
                    # Рисуем прямоугольник между двумя точками
                    cv2.rectangle(img, pt1, pt2, (255, 0, 0), 2)
                    # Выбираем позицию для подписи – в верхнем левом углу прямоугольника
                    label_x = min(pt1[0], pt2[0])
                    label_y = min(pt1[1], pt2[1])
                    cv2.putText(img, str(shape_index), (label_x + 5, label_y + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_click = []  # сброс для следующего прямоугольника
            elif mode == 'ellipse':
                current_click.append((x, y))
                if len(current_click) == 1:
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(current_click) == 2:
                    shape_index += 1
                    pt1, pt2 = current_click[0], current_click[1]
                    # Вычисляем центр и полуоси эллипса (эллипс вписывается в прямоугольник)
                    center_x = int((pt1[0] + pt2[0]) / 2)
                    center_y = int((pt1[1] + pt2[1]) / 2)
                    axis_x = abs(pt2[0] - pt1[0]) // 2
                    axis_y = abs(pt2[1] - pt1[1]) // 2
                    shapes.append({'index': shape_index, 'pt1': pt1, 'pt2': pt2,
                                   'center': (center_x, center_y), 'axes': (axis_x, axis_y)})
                    cv2.ellipse(img, (center_x, center_y), (axis_x, axis_y), 0, 0, 360, (0, 255, 255), 2)
                    # Подписываем эллипс номером (номер выводим в центре)
                    cv2.putText(img, str(shape_index), (center_x - 10, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_click = []
            cv2.imshow("Image", img)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", click_event)
    
    print("Левая кнопка мыши для выбора фигур.")
    print("Нажмите ESC для завершения выбора (окно с изображением должно быть активным).")

    # Ждем нажатия ESC для завершения выбора
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            # Если есть незавершённая фигура (например, один клик для прямоугольника или эллипса),
            # сбрасываем её:
            if mode in ['rectangle', 'ellipse'] and current_click:
                print("Незавершённая фигура отброшена.")
                current_click = []
            break
    cv2.destroyAllWindows()

    # Формирование данных для сохранения в Excel
    if mode == 'point':
        if not shapes:
            print("Нет выбранных точек.")
            return
        data = {"Index": [], "Image": [], "X": [], "Y": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(image_path)
            data["X"].append(s['x'])
            data["Y"].append(s['y'])
    elif mode == 'rectangle':
        if not shapes:
            print("Нет выбранных прямоугольников.")
            return
        data = {"Index": [], "Image": [], "X1": [], "Y1": [], "X2": [], "Y2": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(image_path)
            data["X1"].append(s['pt1'][0])
            data["Y1"].append(s['pt1'][1])
            data["X2"].append(s['pt2'][0])
            data["Y2"].append(s['pt2'][1])
    elif mode == 'ellipse':
        if not shapes:
            print("Нет выбранных эллипсов.")
            return
        data = {"Index": [], "Image": [],
                "CenterX": [], "CenterY": [],
                "AxisX": [], "AxisY": [],
                "Pt1X": [], "Pt1Y": [],
                "Pt2X": [], "Pt2Y": []}
        for s in shapes:
            data["Index"].append(s['index'])
            data["Image"].append(image_path)
            data["CenterX"].append(s['center'][0])
            data["CenterY"].append(s['center'][1])
            data["AxisX"].append(s['axes'][0])
            data["AxisY"].append(s['axes'][1])
            data["Pt1X"].append(s['pt1'][0])
            data["Pt1Y"].append(s['pt1'][1])
            data["Pt2X"].append(s['pt2'][0])
            data["Pt2Y"].append(s['pt2'][1])
    
    df = pd.DataFrame(data)
    try:
        df.to_excel(excel_file, index=False)
        print(f"Результаты сохранены в файле {excel_file}")
    except Exception as e:
        print("Ошибка при сохранении Excel файла:", e)

# Пример использования:
if __name__ == "__main__":
    # Возможные режимы: 'point', 'rectangle', 'ellipse'
    # Для выбора прямоугольников:
    image_file = r"G:\My\sov\extract\Spores\original_img\best\4x\A best_4x_1_scale.png"
    excel_file = r"G:\My\sov\extract\Spores\original_img\test\result.xlsx"
    excel_file_p = r"G:\My\sov\extract\Spores\original_img\test\result_p.xlsx"
    # Выбор одной точки:
    # select_points_or_rectangles(image_file, mode='point', excel_file=excel_file)
    select_shapes(image_file, mode='rectangle', excel_file=excel_file_p)
   
    # select_shapes(image_file, mode='rectangle', excel_file=excel_file_p)
    # Для выбора точек:
    # select_shapes("path/to/your/image.jpg", mode='point', excel_file='points_results.xlsx')
    # Для выбора эллипсов:
    # select_shapes("path/to/your/image.jpg", mode='ellipse', excel_file='ellipses_results.xlsx')
