import cv2
import pandas as pd

def select_point_or_rectangle(image_path, mode='point', excel_file='results.xlsx'):
    """
    Функция загружает изображение, позволяет выбрать точку или прямоугольник,
    и сохраняет имя файла и координаты выбранных точек в Excel.
    
    Параметры:
      image_path  - путь к изображению
      mode        - режим работы: 'point' для одной точки, 'rectangle' для прямоугольника (две точки)
      excel_file  - имя файла Excel для сохранения результата
    """
    # Загружаем изображение и создаём копию для отрисовки
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка: не удалось загрузить изображение!")
        return
    clone = img.copy()
    points = []

    def click_event(event, x, y, flags, param):
        nonlocal points, img
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            if mode == 'point':
                # Отметка выбранной точки
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            elif mode == 'rectangle':
                if len(points) == 1:
                    # Отмечаем первую точку
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
                elif len(points) == 2:
                    # Отмечаем вторую точку и рисуем прямоугольник между ними
                    cv2.rectangle(img, points[0], points[1], (0, 255, 0), 2)
            cv2.imshow("Image", img)

    # Отображаем изображение и регистрируем обработчик кликов
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", click_event)

    print("Нажмите левой кнопкой мыши для выбора точки(ей).")
    print("Нажмите ESC для отмены (или если закончите выбор).")

    # Ждем, пока пользователь не сделает нужное количество кликов или не нажмет ESC
    while True:
        key = cv2.waitKey(1) & 0xFF
        if mode == 'point' and len(points) >= 1:
            break
        if mode == 'rectangle' and len(points) >= 2:
            break
        if key == 27:  # ESC
            break

    cv2.destroyAllWindows()

    # Если не выбрано нужное количество точек, завершаем функцию
    if (mode == 'point' and len(points) < 1) or (mode == 'rectangle' and len(points) < 2):
        print("Выбор не завершён.")
        return

    # Подготовка данных для Excel
    if mode == 'point':
        data = {
            "Image": [image_path],
            "X": [points[0][0]],
            "Y": [points[0][1]]
        }
    elif mode == 'rectangle':
        data = {
            "Image": [image_path],
            "X1": [points[0][0]],
            "Y1": [points[0][1]],
            "X2": [points[1][0]],
            "Y2": [points[1][1]]
        }
    df = pd.DataFrame(data)
    
    # Сохранение данных в Excel (для работы требуется установленный openpyxl)
    try:
        df.to_excel(excel_file, index=False)
        print(f"Результаты сохранены в файле {excel_file}")
    except Exception as e:
        print("Ошибка при сохранении Excel файла:", e)

# Пример использования:
if __name__ == "__main__":
    image_file = r"G:\My\sov\extract\Spores\original_img\best\4x\A best_4x_1_scale.png"
    excel_file = r"G:\My\sov\extract\Spores\original_img\test\result.xlsx"
    # Выбор одной точки:
    select_point_or_rectangle(image_file, mode='point', excel_file=excel_file)
    
    # Выбор прямоугольника (две точки):
    # select_point_or_rectangle("path/to/your/image.jpg", mode='rectangle', excel_file='result_rectangle.xlsx')
