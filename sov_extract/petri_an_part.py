import cv2
import numpy as np

def analyze_particles(image_path, min_area=50, max_area=10000, show_result=True):
    """
    Выполняет сегментацию и анализ частиц на изображении.
    
    Параметры:
      image_path (str): путь к изображению.
      min_area (float): минимальная площадь для фильтрации найденных контуров (по умолчанию 50).
      max_area (float): максимальная площадь для фильтрации найденных контуров (по умолчанию 10000).
      show_result (bool): если True, отображает промежуточные и итоговые изображения.
    
    Возвращает:
      particles_info (list): список словарей с информацией о найденных частицах (площадь, ограничивающий прямоугольник, контур).
      thresh_image (numpy.ndarray): бинаризированное (черно-белое) изображение.
      annotated_image (numpy.ndarray): исходное изображение с нарисованными контурами и bounding box.
    """
    # Загружаем изображение
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Изображение по пути {image_path} не найдено.")
    
    # Переводим изображение в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Применяем пороговую обработку с использованием метода Отсу
    # cv2.threshold вернёт оптимальное пороговое значение ret и бинаризированное изображение thresh
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Если объекты представлены тёмными областями на светлом фоне, можно инвертировать изображение:
    # thresh = cv2.bitwise_not(thresh)
    
    # Находим контуры (используем RETR_EXTERNAL, чтобы взять только внешние контуры)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    particles_info = []
    # Создаём копию исходного изображения для аннотаций
    annotated_image = image.copy()
    
    # Проходим по всем найденным контурам
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Фильтруем по площади
        if area < min_area or area > max_area:
            continue
        
        # Получаем ограничивающий прямоугольник для контура
        x, y, w, h = cv2.boundingRect(cnt)
        # Сохраняем информацию о частице
        particle = {
            'area': area,
            'bounding_box': (x, y, w, h),
            'contour': cnt
        }
        particles_info.append(particle)
        
        # Рисуем контур (зелёным) и ограничивающий прямоугольник (синим)
        cv2.drawContours(annotated_image, [cnt], -1, (0, 255, 0), 2)
        cv2.rectangle(annotated_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Отображаем результаты, если требуется
    if show_result:
        cv2.imshow("Binary (Thresholded) Image", thresh)
        cv2.imshow("Annotated Image", annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return particles_info, thresh, annotated_image

# Пример использования функции:
if __name__ == "__main__":
    # Укажите путь к вашему изображению
    image_path = "path/to/your/image.jpg"
    particles, binary_img, annotated_img = analyze_particles(image_path, min_area=50, max_area=10000, show_result=True)
    
    print(f"Найдено частиц: {len(particles)}")
    for idx, particle in enumerate(particles, start=1):
        print(f"Частица {idx}: площадь = {particle['area']:.2f}, bounding box = {particle['bounding_box']}")
