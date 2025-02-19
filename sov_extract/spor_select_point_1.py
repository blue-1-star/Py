import cv2
import pandas as pd

def select_points_or_rectangles(image_path, mode='point', excel_file='results.xlsx'):
    """
    Функция загружает изображение, позволяет выбрать точки или прямоугольники с помощью мыши,
    и сохраняет имя файла изображения и координаты выбранных объектов в Excel.
    
    Параметры:
      image_path  - путь к изображению.
      mode        - режим работы: 'point' для выбора точек, 'rectangle' для выбора прямоугольников.
      excel_file  - имя Excel файла для сохранения результатов.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка: не удалось загрузить изображение!")
        return
    clone = img.copy()
    
    # В зависимости от режима будем хранить результаты.
    if mode == 'point':
        points = []
    elif mode == 'rectangle':
        rectangles = []        # Список для сохранения прямоугольников (каждый в виде ((x1, y1), (x2, y2)))
        current_click = []     # Временное хранение точек для текущего прямоугольника
    else:
        print("Неизвестный режим. Используйте 'point' или 'rectangle'.")
        return
    
    def click_event(event, x, y, flags, param):
        nonlocal points, rectangles, current_click, img
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode == 'point':
                points.append((x, y))
                # Отметка выбранной точки
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(img, f"{len(points)}", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            elif mode == 'rectangle':
                current_click.append((x, y))
                if len(current_click) == 1:
                    # Отмечаем первую точку
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(current_click) == 2:
                    # Отмечаем вторую точку и рисуем прямоугольник между ними
                    cv2.rectangle(img, current_click[0], current_click[1], (0, 255, 0), 2)
                    rectangles.append((current_click[0], current_click[1]))
                    current_click = []  # Сбрасываем для следующего прямоугольника
            cv2.imshow("Image", img)
    
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", click_event)
    
    print("Левая кнопка мыши для выбора точек/прямоугольников.")
    print("Нажмите ESC для завершения выбора.")
    
    # Ждем, пока пользователь не нажмет ESC
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()
    
    # Сохранение результатов в Excel
    if mode == 'point':
        if not points:
            print("Нет выбранных точек.")
            return
        # Подготавливаем данные: каждая точка в отдельной строке
        data = {"Image": [], "X": [], "Y": []}
        for pt in points:
            data["Image"].append(image_path)
            data["X"].append(pt[0])
            data["Y"].append(pt[1])
        df = pd.DataFrame(data)
    elif mode == 'rectangle':
        if not rectangles:
            print("Нет выбранных прямоугольников.")
            return
        # Подготавливаем данные: каждая пара точек (прямоугольник) в отдельной строке
        data = {"Image": [], "X1": [], "Y1": [], "X2": [], "Y2": []}
        for rect in rectangles:
            pt1, pt2 = rect
            data["Image"].append(image_path)
            data["X1"].append(pt1[0])
            data["Y1"].append(pt1[1])
            data["X2"].append(pt2[0])
            data["Y2"].append(pt2[1])
        df = pd.DataFrame(data)
    
    try:
        df.to_excel(excel_file, index=False)
        print(f"Результаты сохранены в файле {excel_file}")
    except Exception as e:
        print("Ошибка при сохранении Excel файла:", e)

# Пример использования:
if __name__ == "__main__":
    image_file = r"G:\My\sov\extract\Spores\original_img\best\4x\A best_4x_1_scale.png"
    excel_file = r"G:\My\sov\extract\Spores\original_img\test\result.xlsx"
    excel_file_p = r"G:\My\sov\extract\Spores\original_img\test\result_p.xlsx"
    # Выбор одной точки:
    # select_points_or_rectangles(image_file, mode='point', excel_file=excel_file)
    select_points_or_rectangles(image_file, mode='rectangle', excel_file=excel_file_p)
   
    
    # Для выбора множества прямоугольников:
    # select_points_or_rectangles("path/to/your/image.jpg", mode='rectangle', excel_file='rectangles_results.xlsx')
