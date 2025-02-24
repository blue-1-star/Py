
import cv2
import numpy as np

def region_growing_fixed_seed(img, seed, thresh, display_interval=100, print_interval=1000):
    """
    Region growing algorithm that compares each pixel to the initial seed value.
    
    Parameters:
      img             - Grayscale image.
      seed            - Coordinates of the seed point (x, y).
      thresh          - Threshold for allowable intensity difference.
      display_interval- Number of iterations between screen updates.
      
    Returns:
      mask - Binary mask of the grown region.
    """
    h, w = img.shape
    mask = np.zeros((h, w), np.uint8)
    seed_value = int(img[seed[1], seed[0]])  # Extract pixel value at (x, y), where x is seed[0] and y is seed[1].
    seed_list = [seed]
    mask[seed[1], seed[0]] = 255
    iteration = 0

    # Create a resizable window for process display
    cv2.namedWindow("Process Region Growing", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Process Region Growing", 800, 600)

    while seed_list:
        x, y = seed_list.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                    # Compare new pixel intensity with the initial seed value
                    if abs(int(img[ny, nx]) - seed_value) < thresh:
                        mask[ny, nx] = 255
                        seed_list.append((nx, ny))
        iteration += 1
        if iteration % print_interval == 0:
            print("Iteration:", iteration, "Region size:", np.sum(mask == 255))

        if iteration % display_interval == 0:
            cv2.imshow("Process Region Growing", mask)
            cv2.waitKey(1)
            
    return mask

# Load the input image
image_path = r"G:\My\sov\extract\Spores\original_img\worst\test\A_best_4x_11.png"  # Replace with your image path
img_color = cv2.imread(image_path)
if img_color is None:
    print("Error loading image!")
    exit()

# Convert the image to grayscale
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Mouse click event handler
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x, y)
        print("Seed point selected:", seed)
        seg_mask = region_growing_fixed_seed(img_gray, seed, thresh=10, display_interval=200)
        
        cv2.namedWindow("Final Mask", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Final Mask", 800, 600)
        cv2.imshow("Final Mask", seg_mask)
        
        overlay = img_color.copy()
        overlay[seg_mask == 255] = (0, 0, 255)
        
        cv2.namedWindow("Mask Overlay", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Mask Overlay", 800, 600)
        cv2.imshow("Mask Overlay", overlay)

# Create a resizable window with an English title for seed selection
window_name = "Select Seed Point"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 800, 600)
cv2.imshow(window_name, img_color)
cv2.setMouseCallback(window_name, click_event)

print("Click the left mouse button on the spore to start the region growing algorithm.")
cv2.waitKey(0)
cv2.destroyAllWindows()
