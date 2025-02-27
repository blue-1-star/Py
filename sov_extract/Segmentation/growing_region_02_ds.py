import os
import cv2
import numpy as np
import pandas as pd

def region_growing_fixed_seed(image_path, threshold=15, base_mode='seed'):
    directory = os.path.dirname(image_path)
    graph_dir = os.path.join(directory, 'graph')
    os.makedirs(graph_dir, exist_ok=True)
    
    image = cv2.imread(image_path)
    if image is None:
        print("Ошибка: Не удалось загрузить изображение.")
        return
    
    overlay = image.copy()
    auto_select_regions = []
    region_data = []
    file_name = os.path.basename(image_path)
    window_name = file_name
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1980, 1320)
    
    spore_count = 1
    
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
        cv2.imshow(window_name, overlay)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('n'):
            break
        if key == 27:  # ESC для выхода
            print("Выход из программы")
            break
        
        if key == ord(' ') or key == 13:  # Space или Enter
            roi = cv2.selectROI(window_name, image, fromCenter=False, showCrosshair=True)
            if roi[2] == 0 or roi[3] == 0:
                continue  # Пропускаем, если ничего не выбрано
            
            seed = (int(roi[1] + roi[3] / 2), int(roi[0] + roi[2] / 2))
            mask, iterations = region_growing(seed)
            auto_select_regions.append(mask)
            
            region_area = np.sum(mask == 255)
            seed_rgb = image[seed[0], seed[1]].tolist()
            
            region_data.append([file_name, spore_count, seed[0], seed[1], iterations, seed_rgb, region_area, threshold, base_mode])
            spore_count += 1
            
            overlay[mask == 255] = (0, 255, 0)
            cv2.imshow(window_name, overlay)
    
    cv2.destroyAllWindows()
    
    overlay_path = os.path.join(graph_dir, file_name.replace('.png', '_overlay.png'))
    cv2.imwrite(overlay_path, overlay)
    print(f"Overlay сохранен в: {overlay_path}")
    
    auto_select_path = os.path.join(directory, 'auto_select_region.xlsx')
    df = pd.DataFrame(region_data, columns=["Filename", "Spore Number", "Seed X", "Seed Y", "Iterations", "RGB", "Region Area", "Threshold", "Base Mode"])
    df.to_excel(auto_select_path, index=False)
    print(f"Данные auto_select_region сохранены в: {auto_select_path}")

def process_images_in_directory(directory): 
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp')):
            image_path = os.path.join(directory, filename)
            region_growing_fixed_seed(image_path)

# Пример вызова: process_images_in_directory("path/to/images")
directory = "G:\My\sov\extract\Spores\original_img\grow_reg"
process_images_in_directory(directory)