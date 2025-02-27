import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    window_name = "Выбор спор"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1980, 1320)
    
    def region_growing(seed):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        queue = [seed]
        seed_value = image[seed[0], seed[1]].mean()
        
        while queue:
            x, y = queue.pop()
            if mask[x, y] == 0 and abs(int(image[x, y].mean()) - int(seed_value)) < threshold:
                mask[x, y] = 255
                overlay[x, y] = (0, 255, 0)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < image.shape[0] and 0 <= ny < image.shape[1]:
                        queue.append((nx, ny))
        
        return mask
    
    while True:
        cv2.imshow(window_name, image)
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('n'):
            break
        
        pts = cv2.selectROI(window_name, image, fromCenter=False, showCrosshair=True)
        if pts == (0, 0, 0, 0):
            break
        
        seed = (int(pts[1] + pts[3] / 2), int(pts[0] + pts[2] / 2))
        mask = region_growing(seed)
        auto_select_regions.append(mask)
        region_data.append([seed[0], seed[1], threshold])
        
    cv2.destroyAllWindows()
    
    overlay_path = os.path.join(graph_dir, os.path.basename(image_path).replace('.png', '_overlay.png'))
    cv2.imwrite(overlay_path, overlay)
    print(f"Overlay сохранен в: {overlay_path}")
    
    auto_select_path = os.path.join(directory, 'auto_select_region.xlsx')
    df = pd.DataFrame(region_data, columns=["X", "Y", "Threshold"])
    df.to_excel(auto_select_path, index=False)
    print(f"Данные auto_select_region сохранены в: {auto_select_path}")



directory = "G:\My\sov\extract\Spores\original_img\grow_reg"
# image_path = r"G:\My\sov\extract\Spores\original_img\grow_reg\A_best_4x_11.png"
process_images_in_directory(directory)