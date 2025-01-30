import os
import cv2
import numpy as np
from PIL import Image
from brightness_analysys_2a import process_image
def draw_brightness_area(image, shape='square', size=100):
    """
    Накладывает контур выделенной области на изображение.
    Возвращает обработанное изображение.
    """
    image = np.array(image)
    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2
    
    if shape == 'square':
        top_left = (center_x - size // 2, center_y - size // 2)
        bottom_right = (center_x + size // 2, center_y + size // 2)
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    elif shape == 'circle':
        cv2.circle(image, (center_x, center_y), size // 2, (0, 255, 0), 2)
    
    return Image.fromarray(image)

def save_image_with_contour(image, image_path, output_folder='output'):
    """Сохраняет изображение с контуром."""
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_folder, f"{filename}_imp.png")
    image.save(output_path)
    return output_path



def images_to_pdf(image_paths, pdf_path):
    """Объединяет список изображений в PDF."""
    images = [Image.open(img).convert('RGB') for img in image_paths]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

def process_images_to_pdf(image_paths, pdf_output='output/processed_images.pdf'):
    """
    Обрабатывает список изображений, создавая контуры и PDF.
    """
    processed_images = [draw_brightness_area(img) for img in image_paths]
    images_to_pdf(processed_images, pdf_output)
    print(f'PDF сохранен: {pdf_output}')


image_dir = r"G:\My\sov\extract\ORF\AF"  # Ваш путь к папке с изображениями
current_date = datetime.now().strftime("%d_%m")
output_dir = os.path.join(os.path.dirname(__file__), 'Data')
output_file = os.path.join(output_dir, f"brightness_analys_6_{current_date}.xlsx")
output_pdf = os.path.join(output_dir, f"bright_analys_6_{current_date}.pdf")
lower_threshold = 0
size = 500
cont_folder = f"{image_dir}_contour"


img =  draw_brightness_area(img, shape='square', size=size)
contour_path = save_image_with_contour(img, img_path, output_folder=cont_folder)
contour_paths.append(contour_path) 

